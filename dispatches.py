"""
Handle registration.
"""

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from handlers import start, stop
# from config import questions

# conv_states = {}
# for q in questions:
#     conv_states[q["id"]] = ""

# print(conv_states)

dispatches = [
    CommandHandler("start", start),
    CommandHandler("stop", stop),
    # ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states={
    #         GENDER:
    #         [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
    #         PHOTO: [
    #             MessageHandler(Filters.photo, photo),
    #             CommandHandler('skip', skip_photo)
    #         ],
    #         LOCATION: [
    #             MessageHandler(Filters.location, location),
    #             CommandHandler('skip', skip_location),
    #         ],
    #         BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )
]
