""" handler.py """


import logging
import logging.handlers
import multiprocessing
import multiprocessing.synchronize


class MultiprocessingFileHandler(logging.handlers.RotatingFileHandler):
    """ MultiprocessingFileHandler """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        filename: str,
        lock: multiprocessing.synchronize.Lock,
        maxBytes: int,
        backupCount: int,
        mode: str = "a",
        encoding: str = "utf-8",
        delay: bool = False,
        errors: str = "strict",
    ) -> None:
        """ __init__ """

        super().__init__(
            filename,
            mode,
            maxBytes,
            backupCount,
            encoding,
            delay,
            errors,
        )
        self._lock = lock

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record.
        Output the record to the file, catering for rollover as described
        in doRollover().
        """

        self._lock.acquire()
        try:
            if self.shouldRollover(record):
                self.doRollover()
            logging.FileHandler.emit(self, record)
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
        finally:
            self._lock.release()
