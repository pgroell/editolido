# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Console(object):
    """
    Mock Console class
    """
    def __init__(self, logger):
        self.logger = logger

    # noinspection PyUnusedLocal
    def hud_alert(self, message, icon="success", **kwargs):
        if icon == 'success':
            self.logger.info(message)
        else:
            self.logger.error(message)

    # noinspection PyUnusedLocal
    def alert(self, title, message,
              button1, button2=None, button3=None, hide_cancel_button=False):
        self.logger.error(title)
