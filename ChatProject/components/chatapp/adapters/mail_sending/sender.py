import logging
from typing import Optional

from evraz.classic.components import component

from chatapp.application import interfaces


@component
class FileMailSender(interfaces.MailSender):
    """Simple sender for debugging"""

    logger: Optional[logging.Logger] = None

    def __attrs_post_init__(self):
        if self.logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)

    def send(self, mail: str, title: str, text: str):
        self.logger.info(
            'SendTo: {%s}\n'
            'Title: {%s}\n'
            'Body: {%s}\n',
            mail,
            title,
            text,
        )
