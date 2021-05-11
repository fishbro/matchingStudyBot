import logging

from telegram.ext import Updater

import config
from dispatches import dispatches


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    updater = Updater(config.api_token)

    dp = updater.dispatcher
    for dispatch in dispatches:
        dp.add_handler(dispatch)

    updater.start_polling()

    if not config.username:
        config.username = updater.bot.get_me()["username"]

    logging.info(config.username + " is started!")
    updater.idle()
