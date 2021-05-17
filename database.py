import sqlite3

import config
from config import tables, questions, answers


def _create_string(o):
    t = type(o)
    if t == str:
        return '"%s"' % o
    return str(o)


def create_connection():
    return sqlite3.connect("database.db", isolation_level=None)


def initialize_database():
    cursor = create_connection().cursor()

    for table in tables:
        fields = []
        for field_name in table["schema"]:
            field = table["schema"][field_name]
            fields.append(
                "%s %s %s" %
                (field_name, field["type"], field.get("options", "")))

        cursor.execute("CREATE TABLE IF NOT EXISTS %s (%s)" %
                       (table["name"], ", ".join(fields)))
        fields = cursor.execute("SELECT * FROM %s" % table["name"]).fetchone()
        if fields == None and table["name"] in answers:
            table_name = table["name"]
            print(table_name)
            if table_name != 'skill':
                for ans in answers[table_name]:
                    cursor.execute(
                        'INSERT INTO %s (id, text) VALUES (NULL, "%s")' %
                        (table_name, ans))
            elif table_name == 'skill':
                for ans in answers[table_name]:
                    cursor.execute(
                        'INSERT INTO %s (id,need_help,can_help) VALUES (NULL,"%s","%s")'
                        % (table_name, ans[0], ans[1]))


def get_answers(type):
    return create_connection().cursor().execute("SELECT * FROM %s" %
                                                type).fetchall()


def save_user(user_id, fields):
    user = get_user(user_id)
    user_fields = {
        k: v
        for k, v in fields.items() if k != "can_help" and k != "need_help"
    }
    user_skills = {
        k: v
        for k, v in fields.items() if k == "can_help" or k == "need_help"
    }

    if user == None:
        create_connection().cursor().execute(
            "INSERT INTO users (user_id,%s) VALUES (%d,%s)" %
            (",".join(key for key, value in user_fields.items()), user_id,
             ",".join('"' + str(value) + '"'
                      for key, value in user_fields.items())))

        skills_formated = {}
        skills_list = get_answers('skill')
        for skill in skills_list:
            skills_formated[str(skill[0])] = {'can_help': 0, 'need_help': 0}

        for can, values in user_skills.items():
            for value in values:
                skills_formated[value][can] = 1

        for id, conditions in skills_formated.items():
            create_connection().cursor().execute(
                "INSERT INTO user_skill (user_id,skill_id,%s) VALUES (%d,%s,%s)"
                % (",".join(key
                            for key, value in conditions.items()), user_id, id,
                   ",".join(str(value) for key, value in conditions.items())))
        print('user created')
    else:
        create_connection().cursor().execute(
            "UPDATE users SET %s WHERE user_id=%d" %
            (",".join(key + '="' + str(value) + '"'
                      for key, value in user_fields.items()), user_id))

        skills_formated = {}
        skills_list = get_answers('skill')
        for skill in skills_list:
            skills_formated[str(skill[0])] = {'can_help': 0, 'need_help': 0}

        for can, values in user_skills.items():
            for value in values:
                skills_formated[value][can] = 1

        for id, conditions in skills_formated.items():
            create_connection().cursor().execute(
                "UPDATE user_skill SET %s WHERE user_id=%d and skill_id=%s" %
                (",".join(key + '="' + str(value) + '"'
                          for key, value in conditions.items()), user_id, id))
        print('user saved')


def get_user(user_id):
    return create_connection().cursor().execute(
        "SELECT * FROM users WHERE user_id=%d" % user_id).fetchone()


# def get_user(id):
#     return create_connection().cursor().execute("SELECT * FROM user WHERE user_id=%d" % id).fetchone()

# def get_chat(id):
#     return create_connection().cursor().execute("SELECT * FROM chat WHERE chat_id=%d" % id).fetchone()

# def get_user_chat(user_id, chat_id):
#     return (
#         create_connection()
#         .cursor()
#         .execute("SELECT * FROM user_chat WHERE user_id=%d AND chat_id=%d" % (user_id, chat_id))
#         .fetchone()
#     )

# def get_user_fields(id, fields: list):
#     raw = (
#         create_connection().cursor().execute("SELECT %s FROM user WHERE user_id=%d" % (",".join(fields), id)).fetchone()
#     )
#     result = {}
#     for i in range(len(fields)):
#         result[fields[i]] = raw[i]
#     return result

# def get_user_chat_fields(user_id, chat_id, fields: list):
#     raw = (
#         create_connection()
#         .cursor()
#         .execute("SELECT %s FROM user_chat WHERE user_id=%d AND chat_id=%d" % (",".join(fields), user_id, chat_id))
#         .fetchone()
#     )
#     result = {}
#     for i in range(len(fields)):
#         result[fields[i]] = raw[i]
#     return result

# def create_user(fields: dict):
#     keys = list(fields)
#     return (
#         create_connection()
#         .cursor()
#         .execute(
#             "INSERT INTO user (%s) VALUES (%s)"
#             % (
#                 ",".join(field_name for field_name in keys),
#                 ",".join(_create_string(fields[field_name]) for field_name in keys),
#             )
#         )
#     )

# def create_chat(fields: dict):
#     keys = list(fields)
#     return (
#         create_connection()
#         .cursor()
#         .execute(
#             "INSERT INTO chat (%s) VALUES (%s)"
#             % (
#                 ",".join(field_name for field_name in keys),
#                 ",".join(_create_string(fields[field_name]) for field_name in keys),
#             )
#         )
#     )

# def create_user_chat(fields: dict):
#     keys = list(fields)
#     return (
#         create_connection()
#         .cursor()
#         .execute(
#             "INSERT INTO user_chat (%s) VALUES (%s)"
#             % (
#                 ",".join(field_name for field_name in keys),
#                 ",".join(_create_string(fields[field_name]) for field_name in keys),
#             )
#         )
#     )

# def modify_score(user_id, chat_id, score):
#     return (
#         create_connection()
#         .cursor()
#         .execute("UPDATE user_chat SET score=%d WHERE user_id=%d AND chat_id=%d" % (score, user_id, chat_id))
#     )

initialize_database()
