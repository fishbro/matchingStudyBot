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
        "type": "varchar"
    }
}

shown_schema = {
    "user_id": {
        "type": "INTEGER",
        "options": "PRIMARY KEY"
    },
    "shown_id": {
        "type": "INTEGER",
    }
}

approve_schema = {
    "user_id": {
        "type": "INTEGER",
        "options": "PRIMARY KEY"
    },
    "confirming_id": {
        "type": "INTEGER",
    },
    "is_confirmed": {
        "type": "boolean",
    }
}

additional_schemas = []
checkbox_schemas = []

checkboxes = {}
questions = {}
answers = {}

with open('questions.json') as json_file:
    json_data = json.load(json_file)
    questions = json_data["questions"]
    answers = json_data["answers"]

for q in questions:
    if q['type'] == 'text':
        user_schema[q['id']] = {"type": "varchar"}
    if q['type'] == 'radio':
        user_schema[q['id']] = {"type": "INTEGER"}
        answers_schema = {
            "name": q['answers'],
            "schema": {
                "id": {
                    "type": "INTEGER",
                    "options": "PRIMARY KEY AUTOINCREMENT"
                },
                "text": {
                    "type": "varchar",
                },
            }
        }
        additional_schemas.append(answers_schema)
    if q['type'] == 'checkbox':
        if checkboxes.get(q['answers']) == None:
            checkboxes[q['answers']] = []

        checkboxes[q['answers']].append(q['id'])

for ck in checkboxes.keys():
    additional_schema = {
        "user_id": {
            "type": "INTEGER",
        },
        ck + '_id': {
            "type": "INTEGER",
        }
    }
    answers_schema = {
        "name": ck,
        "schema": {
            "id": {
                "type": "INTEGER",
                "options": "PRIMARY KEY AUTOINCREMENT"
            }
        }
    }
    for ans in checkboxes[ck]:
        additional_schema[ans] = {
            "type": "boolean",
        }
        answers_schema['schema'][ans] = {
            "type": "varchar",
        }
    additional_schemas.append({
        "name": 'user_' + ck,
        "schema": additional_schema
    })
    additional_schemas.append(answers_schema)

tables = [{
    "name": "users",
    "schema": user_schema
}, {
    "name": "shown",
    "schema": shown_schema
}, {
    "name": "approve",
    "schema": approve_schema
}] + additional_schemas

# print(tables)
