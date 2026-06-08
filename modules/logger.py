"""_summary_."""

import logging


class MyLogger:
    """_summary_."""

    def __init__(
        self,
        *,
        logger_name: str = __name__,
        level: int = logging.DEBUG,
        is_logging: bool = False,
    ) -> None:
        """_summary_.

        :param logger_name: _description_, defaults to __name__
        :type logger_name: str, optional
        :param level: _description_, defaults to logging.DEBUG
        :type level: int, optional
        :param is_logging: _description_, defaults to False
        :type is_logging: bool, optional
        """
        self.logger = logging.getLogger(logger_name)

        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S",
        )

        self.is_logging = is_logging

    def debug(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.critical(msg)

    def exception(self, msg: str) -> None:
        """_summary_.

        :param msg: _description_
        :type msg: str
        """
        if self.is_logging:
            self.logger.exception(msg)
