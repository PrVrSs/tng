import logging
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.utils.requires_auth import requires_auth


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


@requires_auth
def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="*bold* _italic_ `fixed width font` [link](http://google.com).",
        parse_mode=telegram.ParseMode.MARKDOWN
    )

    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data='1'),
         InlineKeyboardButton("Option 2", callback_data='2')],
        [InlineKeyboardButton("Option 3", callback_data='3')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id
                          )


def help(bot, update):
    update.message.reply_text("Use /start to test this telegam_connector.")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
