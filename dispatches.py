"""
Handle registration.
"""

from telegram import Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

# conv_states = {}
# for q in questions:
#     conv_states[q["id"]] = ""

# print(conv_states)

PHONE, SUMMARY = range(2)
user_data = {}


def start(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('hello! Your name?')
    # print(update.message)

    return PHONE


def phone(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Your phone?')
    user_data[user["id"]] = {}
    user_data[user["id"]]["name"] = update.message.text
    # print(update.message)

    return SUMMARY


def summary(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[user["id"]]["phone"] = update.message.text
    update.message.reply_text(
        'Your data is: %s' %
        (",".join(user_data[user["id"]][key]
                  for key in user_data[user["id"]].keys())))
    # print(update.message)
    print(user_data)
    user_data[user["id"]] = None

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Bye')
    print(update.message)

    return ConversationHandler.END


dispatches = [
    # CommandHandler("start", start),
    # CommandHandler("stop", stop),
    ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            SUMMARY:
            [MessageHandler(Filters.text & ~Filters.command, summary)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
]
