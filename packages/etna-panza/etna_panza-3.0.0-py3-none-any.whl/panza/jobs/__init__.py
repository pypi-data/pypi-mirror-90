"""
Module providing helpers to manipulate jobs
"""

import json
import logging
import os
import shutil
from subprocess import Popen, PIPE, STDOUT
from typing import Any, Dict

import quixote

from panza import BlueprintLoadError
import panza.build
from panza.cache import Cache
from panza.config import PanzaConfiguration
from panza._utils import augment_syspath, scoped_module_imports

from .docker import DockerDaemon, DockerDaemonSetupError
from .errors import *
from ._pipe_stream import PipeStream
from ._result_serialization import deserialize_result

_LOGGER = logging.getLogger(__name__)

# Add a NullHandler to prevent logging to sys.stderr if logging is not configured by the application
_LOGGER.addHandler(logging.NullHandler())


class ExecutableJobHandle:
    """
    Class representing a job that is ready to be executed
    """

    def __init__(
            self,
            config: PanzaConfiguration,
            job_dir: str,
            env_name: str,
            blueprint: quixote.Blueprint,
            data_path: str
    ):
        self.config = config
        self.job_dir = job_dir
        self.env_name = env_name
        self.blueprint = blueprint
        self.data_path = data_path

    def execute_job(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the job and collect its result

        :param context:         the context to use when calling the inspection steps

        :raise                  panza.errors.JobExecutionError
        """

        volumes = [(self.job_dir, "/moulinette/"), (self.data_path, "/moulinette/rendu/")]

        dockerd = DockerDaemon()
        if self.blueprint.allow_docker is True:
            _LOGGER.info("Starting docker daemon...")
            try:
                dockerd.launch(
                    bridge_ip=self.config.additional_docker_daemon.network_bridge_mask,
                    dns=self.config.additional_docker_daemon.dns,
                )
            except DockerDaemonSetupError:
                _LOGGER.error(f"Unable to execute inspection phase for job {os.path.basename(self.job_dir)}")
                raise
            volumes.append((dockerd.socket_path(), "/var/run/docker.sock"))

        volumes = map(lambda vol: f"-v{vol[0]}:{vol[1]}", volumes)

        try:
            os.mkdir(f"{self.job_dir}/workdir")

            with open(f"{self.job_dir}/context.json", 'w') as context_file:
                json.dump(context, context_file)

            if self.blueprint.allow_docker is True:
                _LOGGER.debug("Waiting for Docker Daemon to start...")
                dockerd.wait_until_started(wait_for_seconds=self.config.additional_docker_daemon.max_wait_time)

            _LOGGER.info("Running inspections in the job's environment...")
            inspector_process = Popen(
                ["docker", "run", "--rm", *volumes, self.env_name, "panza_executor.py"],
                stderr=STDOUT,
                stdout=PIPE,
            )
            with inspector_process:
                _LOGGER.debug("Inspection output:")
                try:
                    for line in PipeStream(inspector_process.stdout).iter_lines(with_timeout=self.config.job_timeout):
                        _LOGGER.debug("  " + line.decode().rstrip())
                except TimeoutError:
                    inspector_process.kill()
                    raise JobExecutionTimeout(self.config.job_timeout)

            return_code = inspector_process.returncode
            if return_code != 0:
                raise InspectionError(f"inspector process exited with error status {return_code}")

            try:
                with open(f"{self.job_dir}/result.json", 'r') as result_file:
                    job_result = deserialize_result(result_file)
            except (json.JSONDecodeError, OSError) as e:
                _LOGGER.error(f"Unable to load the result file: {e}")
                raise ResultLoadingError(e)

            if "error" in job_result:
                raise InspectionError(job_result["error"]["message"])
            return job_result["success"]
        finally:
            if self.blueprint.allow_docker is True:
                _LOGGER.info("Stopping docker daemon...")
                dockerd.stop()


def _sanitize_filename(name: str) -> str:
    import string
    from functools import reduce
    allowed_chars = string.ascii_lowercase + string.digits
    name = map(lambda x: x if x in allowed_chars else '_', name.lower())
    return reduce(lambda acc, x: (acc + x) if x != '_' or (len(acc) > 0 and acc[-1] != '_') else acc, name, "")


class DataAwaitingJobHandle:
    """
    Class representing a job whose environment is already built, and needs to fetch data to operate on
    """

    def __init__(self, config: PanzaConfiguration, job_dir: str, env_name: str, blueprint: quixote.Blueprint):
        self.config = config
        self.job_dir = job_dir
        self.env_name = env_name
        self.blueprint = blueprint

    def _fetch_data(self, fetcher, job_name: str):
        try:
            fetcher()
        except Exception as e:
            _LOGGER.error(f"Unable to fetch data for job {job_name}")
            raise DataFetchingError(e)

    def _fetch_data_from_cache(self, fetcher, delivery_path: str, job_name: str):
        _LOGGER.debug(f"Looking for a cached directory: '{delivery_path}'")
        if not os.path.isdir(delivery_path):
            _LOGGER.debug(f"No cache directory found, fetching data")
            return self._fetch_data(fetcher, job_name)
        _LOGGER.debug(f"Using cached directory '{delivery_path}'")

    def fetch_data(self, context: Dict[str, Any], *, cache: Cache) -> ExecutableJobHandle:
        """
        Fetch the data on which this job will operate
        The fetcher functions specified in the blueprint will be used

        :param context:         the context to use when calling the fetch steps
        :param cache:           the cache to use to store fetched data

        :raise                  panza.errors.DataFetchingError
        """

        job_name = os.path.basename(self.job_dir)
        entry_name = f"{job_name}_{_sanitize_filename(context['request_date'])}"
        resources_path = os.path.join(self.job_dir, "resources")
        _LOGGER.info(f"Fetching data for job {job_name}")
        if not all(f.cached for f in self.blueprint.fetchers):
            _LOGGER.debug(f"Forcing re-fetch of uncached fetchers")
            cache.remove_entry(entry_name)
        if not cache.has_entry(entry_name):
            with cache.add_entry(entry_name) as path:
                _LOGGER.debug(f"No cache directory found, fetching data to '{path}'")
                with augment_syspath([self.job_dir]):
                    with quixote.new_context(
                            **context,
                            delivery_path=path,
                            resources_path=resources_path
                    ):
                        for fetcher in self.blueprint.fetchers:
                            self._fetch_data(fetcher, job_name)
                return ExecutableJobHandle(self.config, self.job_dir, self.env_name, self.blueprint, path)
        path = cache.get_entry(entry_name)
        _LOGGER.debug(f"Reusing cached data from directory '{path}'")
        return ExecutableJobHandle(self.config, self.job_dir, self.env_name, self.blueprint, path)


class JobWorkspaceHandle:
    """
    Class representing a job workspace, that is, a job with its working directory and its resources
    """

    def __init__(self, config: PanzaConfiguration, job_dir: str, blueprint: quixote.Blueprint):
        self.config = config
        self.job_dir = job_dir
        self.blueprint = blueprint

    def __enter__(self):
        return self

    def cleanup(self):
        """
        Cleanup the job's working directory
        """
        job_name = os.path.basename(self.job_dir)
        _LOGGER.info(f"Cleaning up job {job_name}...")
        shutil.rmtree(self.job_dir)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def build_job_environment(self, env_name: str) -> DataAwaitingJobHandle:
        """
        Build the environment specified by the blueprint for this job.
        The builder functions specified in the blueprint will be used to build a suitable Docker image

        :param env_name:        the name to give to the resulting environment

        :raise                  panza.errors.EnvironmentBuildError
        """

        try:
            _LOGGER.info(f"Building environment {env_name}...")
            with augment_syspath([self.job_dir]):
                generator = panza.build.DockerScriptGenerator(self.config.base_image)
                generator.generate_to_file(
                    self.blueprint,
                    os.path.join(self.job_dir, "Dockerfile"),
                    extra_context={"resources_path": os.path.join(self.job_dir, "resources")}
                )
            extra_build_args = []
            if self.config.always_pull is True:
                extra_build_args.append("--pull")
            build_process = Popen(
                ["docker", "build", *extra_build_args, "-t", env_name, self.job_dir],
                stderr=STDOUT,
                stdout=PIPE,
            )
            _LOGGER.debug("Docker builder output:")
            for line in build_process.stdout:
                _LOGGER.debug("  " + line.decode().rstrip())
            return_code = build_process.wait()
            if return_code != 0:
                raise RuntimeError(f"builder process exited with error status {return_code}")
            _LOGGER.debug("Cleaning up after building...")
            os.remove(os.path.join(self.job_dir, "Dockerfile"))
        except Exception as e:
            _LOGGER.error(f"unable to build environment {env_name}: {str(e)}")
            raise EnvironmentBuildError(e)
        return DataAwaitingJobHandle(self.config, self.job_dir, env_name, self.blueprint)


def new_job_workspace(config: PanzaConfiguration, job_files_dir: str, job_name: str) -> JobWorkspaceHandle:
    """
    Create a workspace in which the job can be executed.
    This will create a directory, copy the required files, and load the blueprint

    :param config:              the configuration to use for this job
    :param job_files_dir:       the path to the directory containing the job's resources files
    :param job_name:            the name of the job, used to create its workspace

    :raise                      panza.errors.WorkspaceCreationError
    """

    job_dir = os.path.normpath(os.path.join(config.root_directory, job_name))
    _LOGGER.info(f"Creating workspace {job_dir} for job {job_name}...")

    try:
        shutil.copytree(job_files_dir, job_dir)
    except OSError as e:
        raise WorkspaceCreationError(e)

    _LOGGER.info(f"Loading blueprint for job {job_name}...")

    try:
        with augment_syspath([job_dir]):
            with scoped_module_imports():
                blueprint = panza.BlueprintLoader.load_from_directory(job_dir)
    except BlueprintLoadError as e:
        shutil.rmtree(job_dir)
        raise WorkspaceCreationError(e)

    return JobWorkspaceHandle(config, job_dir, blueprint)
