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
        "type": "int",
        "options": "PRIMARY KEY"
    },
    "username": {
        "type": "TEXT"
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
        user_schema[q['id']] = {"type": "TEXT"}
    if q['type'] == 'radio':
        user_schema[q['id']] = {"type": "int"}
        answers_schema = {
            "name": q['answers'],
            "schema": {
                "id": {
                    "type": "int",
                    "options": "PRIMARY KEY"
                },
                "text": {
                    "type": "TEXT",
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
            "type": "int",
        },
        ck + '_id': {
            "type": "int",
        }
    }
    answers_schema = {
        "name": ck,
        "schema": {
            "id": {
                "type": "int",
                "options": "PRIMARY KEY"
            }
        }
    }
    for ans in checkboxes[ck]:
        additional_schema[ans] = {
            "type": "boolean",
        }
        answers_schema['schema'][ans] = {
            "type": "TEXT",
        }
    additional_schemas.append({
        "name": 'user_' + ck,
        "schema": additional_schema
    })
    additional_schemas.append(answers_schema)

tables = [{"name": "users", "schema": user_schema}] + additional_schemas

# print(tables)
