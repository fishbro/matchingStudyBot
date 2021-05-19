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


def save_user(user_raw, fields):
    user = get_user(user_raw['id'])
    username = user_raw['username']
    user_id = user_raw['id']

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
            'INSERT INTO users (user_id,username,%s) VALUES (%d,"%s",%s)' %
            (",".join(key for key, value in user_fields.items()), user_id,
             username, ",".join('"' + str(value) + '"'
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
            'UPDATE users SET username="%s",%s WHERE user_id=%d' %
            (username, ",".join(
                key + '="' + str(value) + '"'
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
    fields = {}
    cursor = create_connection().cursor()
    raw_values = cursor.execute("SELECT * FROM users WHERE user_id=%d" %
                                user_id).fetchone()
    if raw_values == None:
        return None

    cols = cursor.execute(
        "SELECT name FROM PRAGMA_TABLE_INFO('users')").fetchall()
    # skills = get_skills(user_id)

    for key, value in enumerate(list(raw_values)):
        fields[cols[key][0]] = value

    # return ({**fields, **skills})
    return fields


def get_users_by_params(params):
    cursor = create_connection().cursor()
    ids_raw = list(
        cursor.execute(
            "SELECT user_id FROM users WHERE %s" %
            " AND ".join(param + '="' + str(value) + '"'
                         for param, value in params.items())).fetchall())

    if ids_raw == None:
        return []

    ids = [el[0] for el in ids_raw]

    return ids


def get_users_by_skills(raw_skills):
    cursor = create_connection().cursor()
    query = []
    user_skills = {
        "need_help": raw_skills["can_help"],
        "can_help": raw_skills["need_help"]
    }

    for type, skills in user_skills.items():
        for skill in skills:
            query.append('(skill_id="%d" AND %s="1")' % (skill, type))

    ids_raw = cursor.execute("SELECT user_id FROM user_skill WHERE %s" %
                             " OR ".join(param for param in query)).fetchall()

    if ids_raw == None:
        return {}

    ids_w = {}
    for el in list(ids_raw):
        if el[0] in ids_w:
            ids_w[el[0]] = ids_w[el[0]] + 1
        else:
            ids_w[el[0]] = 1

    return ids_w


def get_skills(user_id):
    skills = {"need_help": [], "can_help": []}
    rows = create_connection().cursor().execute(
        "SELECT skill_id,need_help,can_help FROM user_skill WHERE user_id=%d" %
        user_id).fetchall()

    for row in rows:
        if row[1]:
            skills["need_help"].append(row[0])
        if row[2]:
            skills["can_help"].append(row[0])

    return skills


def shown_add(user_id, shown_id):
    create_connection().cursor().execute(
        'INSERT INTO shown (user_id,shown_id) VALUES (%d,%d)' %
        (user_id, shown_id))


def shown_check(user_id, shown_id):
    rows = create_connection().cursor().execute(
        "SELECT * FROM shown WHERE user_id=%d AND shown_id=%d" %
        (user_id, shown_id)).fetchall()

    return True if rows != None and len(
        rows) > 0 else False  #true if already shown


def shown_remove(shown_id):
    create_connection().cursor().execute(
        'DELETE FROM shown WHERE shown_id=%d' % shown_id)


def get_next(user_id):
    user_params = get_user(user_id)
    user_skills = get_skills(user_id)
    if user_params["relationship_goal"] == 1:
        next_params = {
            "relationship_goal": user_params["relationship_goal"],
            "current_work_scope": user_params["next_work_scope"],
            "next_work_scope": user_params["current_work_scope"],
        }
    else:
        next_params = {
            "relationship_goal": user_params["relationship_goal"],
            "next_work_scope": user_params["next_work_scope"],
        }

    users_by_params = get_users_by_params(next_params)
    match_users = {
        id: count
        for id, count in get_users_by_skills(user_skills).items()
        if id != user_id and id in users_by_params
        and not shown_check(user_id, id)
    }

    match_users_sorted = [
        k for k in sorted(match_users, key=match_users.get, reverse=True)
    ]

    if len(match_users_sorted) > 0:
        shown_add(user_id, match_users_sorted[0])
        return match_users_sorted[0]
    else:
        return None


initialize_database()
