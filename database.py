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
