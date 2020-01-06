from telegram.ext import CommandHandler, CallbackQueryHandler
from app.connector.telegam_connector import BaseBotCreator
from app.connector.telegam_connector.handlers import *


REQUEST_KWARGS = {
    'proxy_url': 'socks5://127.0.0.1:9050'
}


def main():

    bot: BaseBotCreator = BaseBotCreator(
        token='',
        request_kwargs=REQUEST_KWARGS,
        admin_username='',
    )

    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CallbackQueryHandler(button))
    bot.add_handler(CommandHandler('help', help))

    bot.add_error_handler(error)

    bot.start()


if __name__ == '__main__':
    main()
