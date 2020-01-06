import os
import sys
from threading import Thread
from telegram.ext import Updater, CommandHandler, Filters
from app.connector.telegam_connector import IBotCreator


class BaseBotCreator(IBotCreator):

    def __init__(self, token: str='', request_kwargs: dict=None, admin_username: str=''):

        self._updater: Updater = Updater(token=token, request_kwargs=request_kwargs)

        self.add_handler(CommandHandler(
            'r',
            self._restart,
            filters=Filters.user(username=admin_username)
        ))

    def add_handler(self, handler) -> None:
        self._updater.dispatcher.add_handler(handler)

    def add_error_handler(self, handler) -> None:
        self._updater.dispatcher.add_error_handler(handler)

    def start(self) -> None:
        self._updater.start_polling()
        self._updater.idle()

    def _stop_and_restart(self) -> None:
        self._updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _restart(self, bot, update) -> None:
        update.message.reply_text('Bot is restarting...')
        Thread(target=self._stop_and_restart).start()
