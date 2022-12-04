import datetime
import sqlite3
con = sqlite3.connect("db.sqlite3",check_same_thread=False)
cur = con.cursor()


def last_activity(email):
    dt = datetime.datetime.now()
    cur.execute(f"UPDATE users_snuser SET last_activity = '{dt}' WHERE email = '{email}'")
    con.commit()

def get_user(username,email):
    if username:
        query = cur.execute(f"SELECT username,password,email FROM users_snuser WHERE username = '{username}'")
    else:
        query = cur.execute(f"SELECT username,password,email FROM users_snuser WHERE email = '{email}'")
    res = query.fetchone()
    print(res)
    return res