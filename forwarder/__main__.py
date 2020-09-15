import importlib

from telegram import Bot, Update
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async

from forwarder import API_KEY, OWNER_ID, WEBHOOK, IP_ADDRESS, URL, CERT_PATH, PORT, LOGGER, \
    updater, dispatcher
from forwarder.modules import ALL_MODULES

PM_START_TEXT = """
Hey {}, I'm {}!

HELP MENU IS LOCKED BY @EBRUISER 💁🏻‍♂️
"""

PM_HELP_TEXT = """
HELP MENU IS LOCKED BY @EBRUISER 💁🏻‍♂️
"""

for module in ALL_MODULES:
    importlib.import_module("forwarder.modules." + module)


@run_async
def start(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]

    if chat.type == "private":
        message.reply_text(PM_START_TEXT.format(user.first_name, dispatcher.bot.first_name), parse_mode=ParseMode.HTML)
    else:
        message.reply_text("I'm up and running!")


@run_async
def help(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not chat.type == "private":
        message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        message.reply_text(PM_HELP_TEXT)


def main():
    start_handler = CommandHandler("start", start, filters=Filters.user(OWNER_ID))
    help_handler = CommandHandler("help", help, filters=Filters.user(OWNER_ID))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen=IP_ADDRESS,
                              port=PORT,
                              url_path=API_KEY)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + API_KEY,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + API_KEY)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
