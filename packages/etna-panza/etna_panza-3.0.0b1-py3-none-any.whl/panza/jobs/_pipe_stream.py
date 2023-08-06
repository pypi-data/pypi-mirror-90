import os
import select
import time
from typing import IO


class PipeStream:
    def __init__(self, stream: IO[bytes]):
        self.stream = stream

    def iter_lines(self, with_timeout: float):
        """
        Obtain a generator that reads the pipe's output line-by-line

        :param with_timeout:            the time (in seconds) to wait before bailing out

        :raise                          TimeoutError
        """
        buf = b""
        timeout_limit = time.monotonic() + with_timeout
        did_timeout = time.monotonic() > timeout_limit
        while not did_timeout:
            read_ready, *_ = select.select([self.stream.fileno()], [], [], 0.5)
            if read_ready:
                data = os.read(self.stream.fileno(), 4096)
                if not data:
                    break
                buf += data
                newline = buf.find(b"\n")
                while newline != -1:
                    line = buf[:newline]
                    buf = buf[newline + 1:]
                    yield line
                    newline = buf.find(b"\n")
            did_timeout = time.monotonic() > timeout_limit
        yield buf
        if did_timeout:
            raise TimeoutError
