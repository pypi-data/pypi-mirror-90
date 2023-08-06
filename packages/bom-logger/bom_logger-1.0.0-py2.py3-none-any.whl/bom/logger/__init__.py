""" __init__.py """


import logging
import logging.config
import logging.handlers
import multiprocessing.synchronize

from bom.configuration.config import Config  # pylint: disable=import-error

from . import formatter  # pylint: disable=import-error
from . import handler  # pylint: disable=import-error


def setup_logger(
    config: Config,
    lock: multiprocessing.synchronize.Lock,  # pylint: disable=unsubscriptable-object
) -> None:
    """ setup_logger """

    assert config

    json_formatter = formatter.JsonFormatter()
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(json_formatter)
    stream_handler.set_name("root_stream_handler")
    file_handler = handler.MultiprocessingFileHandler(
        filename=config.get_string("bomt1me.logger.filename"),
        lock=lock,
        mode="a",
        maxBytes=config.get_int("bomt1me.logger.max_bytes"),
        backupCount=config.get_int("bomt1me.logger.backup_count"),
    )
    file_handler.setFormatter(json_formatter)
    file_handler.set_name(config.get_string("bomt1me.logger.filename"))
    root = logging.getLogger()
    while root.hasHandlers():
        root.removeHandler(root.handlers[0])
    root.addHandler(stream_handler)
    root.addHandler(file_handler)
    root.setLevel(logging.DEBUG)
