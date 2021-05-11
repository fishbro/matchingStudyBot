from telegram import Message, User, Chat
import config
from database import *

# def is_message_for_bot(message: Message):
#     if message.chat.type != "private" and message.text != "/start@%s" % config.username:
#         return False
#     return True

# def is_registered_user(user: User):
#     return True if get_user(user.id) else False
