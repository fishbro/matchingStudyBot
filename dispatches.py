"""
Handle registration.
"""

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from config import questions, answers
from database import get_answers

answers_data = {}
answers_map = {}

PHONE, SUMMARY, RELATIONSHIP, CUR_WORK, CUR_PROFESSION, NEXT_WORK, NEXT_PROFESSION, CAN_HELP, NEED_HELP = range(
    9)
user_data = {}

# ans = get_answers('relationship_goal')
# reply_keyboard = [key[0] for key in ans]
# print(reply_keyboard)

# def button(update: Update, _: CallbackContext):
#     query = update.callback_query
#     # user = update.message.from_user

#     query.answer()

#     data = query.data.split(',')
#     # user_data[user["id"]][data[0]] = data[1]

#     print(data)

#     return SUMMARY


def start(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Напишите свое имя')
    # print(update.message)

    return PHONE


def phone(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[user["id"]] = {}
    user_data[user["id"]]["name"] = update.message.text

    update.message.reply_text('Напишите свой телефон')

    return RELATIONSHIP


def relationship(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[user["id"]]["phone"] = update.message.text

    if answers_data.get('relationship_goal') is None:
        answers_data['relationship_goal'] = get_answers('relationship_goal')

    reply_keyboard = [[
        InlineKeyboardButton(key[1],
                             callback_data='relationship_goal,' + str(key[0]))
        for key in answers_data['relationship_goal']
    ]]
    update.message.reply_text(
        "Ты хочешь общаться с людьми на условиях взаимопомощи или найти человека со схожими потребностями в обучении, чтобы вместе обучаться?",
        reply_markup=InlineKeyboardMarkup(reply_keyboard,
                                          one_time_keyboard=True)),

    return CUR_WORK


def current_work_scope(update: Update, _: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data.split(',')

    user_data[user["id"]]["relationship"] = data[1]
    query.answer()

    if answers_data.get('work_scope') is None:
        answers_data['work_scope'] = get_answers('work_scope')

    reply_keyboard = [[
        InlineKeyboardButton(key[0], callback_data='work_scope,' + str(key[0]))
        for key in answers_data['work_scope']
    ]]
    questions_message = "\n".join(
        str(question[0]) + '. ' + question[1]
        for question in answers_data['work_scope'])
    query.message.reply_text(
        "*Что ж, а теперь давай определимся в какой сфере ты работаешь?*\n\n" +
        questions_message,
        reply_markup=InlineKeyboardMarkup(reply_keyboard,
                                          one_time_keyboard=True),
        parse_mode='Markdown'),

    return CUR_PROFESSION


def current_profession_and_position(update: Update, _: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data.split(',')

    user_data[user["id"]]["relationship"] = data[1]
    query.answer()

    query.message.reply_text('Введите вашу текущую профессию и должность')

    return NEXT_WORK


def next_work_scope(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[
        user["id"]]["current_profession_and_position"] = update.message.text

    if answers_data.get('work_scope') is None:
        answers_data['work_scope'] = get_answers('work_scope')

    reply_keyboard = [[
        InlineKeyboardButton(key[0], callback_data='work_scope,' + str(key[0]))
        for key in answers_data['work_scope']
    ]]
    questions_message = "\n".join(
        str(question[0]) + '. ' + question[1]
        for question in answers_data['work_scope'])
    update.message.reply_text(
        "*Введите желаемую сферу деятельности*\n\n" + questions_message,
        reply_markup=InlineKeyboardMarkup(reply_keyboard,
                                          one_time_keyboard=True),
        parse_mode='Markdown'),

    return NEXT_PROFESSION


def next_profession_and_position(update: Update, _: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data.split(',')

    user_data[user["id"]]["next_work_scope"] = data[1]
    query.answer()

    query.message.reply_text('Введите желаемую сферу деятельности')

    return CAN_HELP


def can_help(update: Update, _: CallbackContext):
    user = update.message.from_user
    user_data[user["id"]]["next_profession_and_position"] = update.message.text

    if answers_data.get('skill') is None:
        answers_data['skill'] = get_answers('skill')

    reply_keyboard = [[
        InlineKeyboardButton(key[0], callback_data='skill,' + str(key[0]))
        for key in answers_data['skill']
    ]]
    questions_message = "\n".join(
        str(question[0]) + '. ' + question[1]
        for question in answers_data['skill'])
    update.message.reply_text(
        "*Прежде чем мы перейдём к вопросу о том, с чем лично тебе нужна помощь, расскажи, пожалуйста, а с чем ты сам мог бы помочь другим? Выбери все возможные варианты:*\n\n"
        + questions_message,
        reply_markup=InlineKeyboardMarkup(reply_keyboard,
                                          one_time_keyboard=True),
        parse_mode='Markdown'),

    return NEED_HELP


def need_help(update: Update, _: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data.split(',')

    user_data[user["id"]]["can_help"] = data[1]
    query.answer()

    if answers_data.get('skill') is None:
        answers_data['skill'] = get_answers('skill')

    reply_keyboard = [[
        InlineKeyboardButton(key[0], callback_data='skill,' + str(key[0]))
        for key in answers_data['skill']
    ]]
    questions_message = "\n".join(
        str(question[0]) + '. ' + question[2]
        for question in answers_data['skill'])
    query.message.reply_text(
        "*Что ж, а теперь давай определимся с чем нужна помощь тебе. Выбери один из вариантов:*\n\n"
        + questions_message,
        reply_markup=InlineKeyboardMarkup(reply_keyboard,
                                          one_time_keyboard=True),
        parse_mode='Markdown'),

    return SUMMARY


def summary(update: Update, _: CallbackContext):
    query = update.callback_query
    user = query.from_user
    data = query.data.split(',')

    user_data[user["id"]]["need_help"] = data[1]
    print(user_data)
    answers_message = "\n".join(key + ': ' + user_data[user["id"]][key]
                                for key in user_data[user["id"]].keys())
    query.message.reply_text(
        "Спасибо за заполнение анкеты, ваши данные: \n\n" + answers_message)

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    update.message.reply_text('Bye')
    print(update.message)

    return ConversationHandler.END


dispatches = [
    # CommandHandler("start", start),
    # CommandHandler("stop", stop),
    # CallbackQueryHandler(button),
    ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)],
            RELATIONSHIP:
            [MessageHandler(Filters.text & ~Filters.command, relationship)],
            CUR_WORK: [CallbackQueryHandler(current_work_scope)],
            CUR_PROFESSION:
            [CallbackQueryHandler(current_profession_and_position)],
            NEXT_WORK:
            [MessageHandler(Filters.text & ~Filters.command, next_work_scope)],
            NEXT_PROFESSION:
            [CallbackQueryHandler(next_profession_and_position)],
            CAN_HELP:
            [MessageHandler(Filters.text & ~Filters.command, can_help)],
            NEED_HELP: [CallbackQueryHandler(need_help)],
            SUMMARY: [CallbackQueryHandler(summary)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
]
