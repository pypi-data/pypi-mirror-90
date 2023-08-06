from contextlib import contextmanager
from tempfile import TemporaryDirectory

import pytest

from panza.cache import Cache


class TestCache:
    @contextmanager
    def setup(self):
        with TemporaryDirectory() as path:
            yield path

    def add_test_entry(self, cache, entry_name: str):
        with cache.add_entry(entry_name) as entry_path:
            with open(f"{entry_path}/file.txt", "w") as f:
                f.write(entry_name)

    def get_test_entry_content(self, cache, entry_name):
        entry_path = cache.get_entry(entry_name)
        with open(f"{entry_path}/file.txt", "r") as f:
            return f.read()

    def refresh_entry(self, cache, entry_name):
        cache.get_entry(entry_name)

    def test_basic(self):
        with self.setup() as path:
            cache = Cache.create_at(f"{path}/cache", max_entries=16)
            assert not cache.has_entry("test")
            with pytest.raises(FileNotFoundError):
                cache.get_entry("test")

            self.add_test_entry(cache, "test")

            assert cache.has_entry("test")
            assert self.get_test_entry_content(cache, "test") == "test"

            cache.remove_entry("test")
            assert not cache.has_entry("test")
            with pytest.raises(FileNotFoundError):
                cache.get_entry("test")

    def test_eviction(self):
        with self.setup() as path:
            cache = Cache.create_at(f"{path}/cache", max_entries=4)

            for entry_name in ("test1", "test2", "test3", "test4"):
                self.add_test_entry(cache, entry_name)

            for entry_name in ("test1", "test2", "test3", "test4"):
                assert cache.has_entry(entry_name)

            self.add_test_entry(cache, "test5")

            for entry_name in ("test2", "test3", "test4", "test5"):
                assert cache.has_entry(entry_name)
                assert self.get_test_entry_content(cache, entry_name) == entry_name

            assert not cache.has_entry("test1")

    def test_refresh(self):
        with self.setup() as path:
            cache = Cache.create_at(f"{path}/cache", max_entries=4)

            for entry_name in ("test1", "test2", "test3", "test4"):
                self.add_test_entry(cache, entry_name)

            for entry_name in ("test1", "test2", "test3", "test4"):
                assert cache.has_entry(entry_name)

            self.refresh_entry(cache, "test1")
            self.add_test_entry(cache, "test5")

            for entry_name in ("test1", "test3", "test4", "test5"):
                assert cache.has_entry(entry_name)
                assert self.get_test_entry_content(cache, entry_name) == entry_name

            assert not cache.has_entry("test2")
