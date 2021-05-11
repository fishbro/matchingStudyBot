"""
Handle registration.
"""

from telegram.ext import CommandHandler
from handlers import start, stop

dispatches = [
    CommandHandler("start", start),
    CommandHandler("stop", stop),
]
