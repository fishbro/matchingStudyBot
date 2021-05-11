"""
Settings and configuration for your bot.
"""
import json
from userconfig import TOKEN

# Bot's API Token granted by the @BotFather
api_token = TOKEN

# This field will be auto-populated
username = None

# A list of user IDs who can manage the bot
admins = []

user_schema = {
    "user_id": {
        "type": "INTEGER",
        "options": "PRIMARY KEY"
    },
    "username": {
        "type": "TEXT"
    }
}

questions = {}

with open('questions.json') as json_file:
    json_data = json.load(json_file)
    questions = json_data["questions"]

for q in questions:
    user_schema[q['id']] = {"type": "TEXT"}

tables = [
    {
        "name": "users",
        "schema": user_schema
    },
]
