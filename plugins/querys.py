import sqlite3


#  TODO change this to use m.status so no need to a sql query and make bot faster and delete this func
def get_admins(chat_id: str, user_id: int):  # get admins to only execute their command
    # get admins from database
    # dbname = str(m.chat.title) + '.db'
    dbname = str(chat_id) + ".db"
    con = sqlite3.connect("databases/" + dbname)  # وصل شدن به دیتا بیس
    cur = con.cursor()
    cur.execute("SELECT num_id FROM USERS WHERE is_admin = (?)", (True,))
    admins = cur.fetchall()
    if (user_id,) in admins:
        return True
    elif not admins:
        return True
    else:
        return False


def new_user(name, username, user_id, status, chat_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute('''INSERT  OR IGNORE INTO USERS VALUES  (?,?,?,?,?,?,?) ''',
                (name, username, user_id, False, 0, status, False))
    con.commit()
    con.close()
    return True


def user_rejoined(user_id, chat_id):  # set status and is_admin to default
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS SET status=(?), is_admin=(?) WHERE main.USERS.num_id = (?)",
                ("member", False, user_id))
    con.commit()
    con.close()
    return True


def verify_user(chat_id, user_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS SET is_verified=(?) WHERE num_id=(?)", (True, user_id))
    con.commit()
    con.close()
    return True


def user_left(chat_id, user_id: int):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS SET 'status' = 'left', is_admin=0 where num_id=:id", {'id': user_id})
    con.commit()
    con.close()
    return True


def add_warns(chat_id, user_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT warn FROM USERS where num_id = (?)", (user_id,))
    warns = cur.fetchone()
    cur.execute("UPDATE USERS SET warn =(?) WHERE num_id=(?)", (warns[0] + 1, user_id), )
    con.commit()
    con.close()
    return True


def del_warns(chat_id, user_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT warn FROM USERS where num_id = (?)", (user_id,))
    warns = cur.fetchone()
    cur.execute("UPDATE USERS SET warn=(?) where num_id=(?)", (warns[0] - 1, user_id,))
    con.commit()
    con.close()
    return True


def ban_user(chat_id, user_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS SET 'status' = 'banned' where num_id=:id", {'id': user_id})
    con.commit()
    con.close()
    return True


def un_ban(chat_id, username):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT num_id FROM USERS WHERE username = (?)", (username,))
    result = cur.fetchone()
    if result is not None:
        cur.execute("UPDATE USERS SET 'status' = 'member' WHERE num_id =(?)", (result[0],))
        return True
    else:
        return False


def promote(chat_id, user_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS SET status = (?) , is_admin=(?)  WHERE num_id = (?)",
                ('administrator', True, user_id))
    con.commit()
    con.close()
    return True


def demote(chat_id, user_id):
    """ignore this"""
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("UPDATE USERS set is_admin=(?),status=(?) where num_id=(?)",
                (False, "member", user_id))
    con.commit()
    con.close()
    return True


def get_setting(chat_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT * FROM SETTING")
    result = cur.fetchall()
    return result


def change_answer(chat_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT * FROM SETTING")
    result = cur.fetchall()

    cur.execute("UPDATE SETTING SET answer_why=(?)", (not result[0][1],))
    con.commit()
    con.close()
    return not result[0][1]


def change_comment(chat_id):
    dbname = str(chat_id) + '.db'
    con = sqlite3.connect("databases/" + dbname)
    cur = con.cursor()
    cur.execute("SELECT * FROM SETTING")
    result = cur.fetchall()

    cur.execute("UPDATE SETTING SET comment_protector=(?)", (not result[0][0],))
    con.commit()
    con.close()
    return not result[0][0]
