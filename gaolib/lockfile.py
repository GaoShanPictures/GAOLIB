# ==============================================================================
# https://github.com/jonasrauber/lockfile
# ==============================================================================
from typing import Union, Optional, Any
import warnings
import os
import time
from pathlib import Path


class Lock:
    """A simple locking mechanism based on lockfiles.

    It creates lockfiles and thus works across different processes and
    different machines with access to the same shared file system as
    long as that file system guarantees atomicity for O_CREAT with O_EXCL.

    Args:
        file_or_lockfile: If it has a ".lock" suffix, it is used as is and will
            be truncated, otherwise a ".lock" suffix is appended.
        timeout: Number of seconds before a TimeoutError is raised. Can be
            None to disable retrying and instead raise a RuntimeError if
            the first attempt fails.
        interval: Number of seconds between each retry.
    """

    def __init__(
        self,
        file_or_lockfile: Union[str, Path],
        timeout: Optional[float] = 20,
        interval: float = 0.05,
    ):
        lockfile = Path(file_or_lockfile)
        if lockfile.suffix != ".lock":
            lockfile = lockfile.with_suffix(lockfile.suffix + ".lock")
        self.lockfile = lockfile
        self.timeout = timeout
        self.interval = interval

        self._lockfile_fd: Optional[int] = None

    @property
    def is_locked(self) -> bool:
        return self._lockfile_fd is not None

    def _acquire(self) -> None:
        assert not self.is_locked
        start_time = time.time()
        while True:
            mode = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_TRUNC
            try:
                fd = os.open(self.lockfile, mode)
            except FileExistsError:
                if self.timeout is None:
                    raise RuntimeError(f"Could not acquire lock on {self.lockfile}")
                if time.time() - start_time >= self.timeout:
                    raise TimeoutError(f"Could not acquire lock on {self.lockfile}")
                time.sleep(self.interval)
            else:
                self._lockfile_fd = fd
                break

    def _release(self) -> None:
        if self.is_locked:
            assert self._lockfile_fd is not None
            os.close(self._lockfile_fd)
            self._lockfile_fd = None
            try:
                os.remove(self.lockfile)
            except FileNotFoundError:
                warnings.warn(f"{self.lockfile} did not exist anymore")

    def __enter__(self) -> None:
        self._acquire()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self._release()

    def __del__(self) -> None:
        self._release()