"""
Handler functions to be dispatched.
"""
# from validators import is_registered_user, is_message_for_bot
import messages


def stop(bot, update):
    # Unsubscribe user from bot
    bot.message.reply_text('bye')


def normal_message(bot, update):
    print("normal")
