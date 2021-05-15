"""
Handle registration.
"""

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
from config import questions, answers
from database import get_answers

answers_data = {}
answers_map = {}

PHONE, SUMMARY, RELATIONSHIP = range(3)
user_data = {}

# ans = get_answers('relationship_goal')
# reply_keyboard = [key[0] for key in ans]
# print(reply_keyboard)


def start(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Напишите свое имя')
    # print(update.message)

    return PHONE


def phone(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Напишите свой телефон')
    user_data[user["id"]] = {}
    user_data[user["id"]]["name"] = update.message.text
    # print(update.message)

    return RELATIONSHIP


def relationship(update: Update, _: CallbackContext):
    user = update.message.from_user

    if answers_data.get('relationship_goal') is None:
        answers_data['relationship_goal'] = get_answers('relationship_goal')

    reply_keyboard = [[key[1] for key in answers_data['relationship_goal']]]
    update.message.reply_text(
        "Ты хочешь общаться с людьми на условиях взаимопомощи или найти человека со схожими потребностями в обучении, чтобы вместе обучаться?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,
                                         one_time_keyboard=True)),
    user_data[user["id"]]["phone"] = update.message.text
    # print(update.message)

    return SUMMARY


def summary(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[user["id"]]["relationship_goal"] = update.message.text
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
            RELATIONSHIP:
            [MessageHandler(Filters.text & ~Filters.command, relationship)],
            SUMMARY:
            [MessageHandler(Filters.text & ~Filters.command, summary)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
]
