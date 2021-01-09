import sqlite3

_connection = None
def get_connection():
    global _connection
    if _connection == None:
        _connection = sqlite3.connect('data.db', check_same_thread=False)
    return _connection

def init_db(force: bool = False):
    conn = get_connection()
    c = conn.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS users')
    c. execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        count_url INT,
        money INT,
        total_money TEXT,
        urls TEXT
    )""")
    conn.commit()

init_db()

def get_count_all_money(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT total_money FROM users WHERE user_id = ?',(str([id]),))
    return c.fetchone()

def update_all_money_plus(id,sum):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET total_money = ? WHERE user_id = ?', (str(sum+int(get_count_all_money(id)[0])), str([id]),))
    conn.commit()

def get_count_url(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT count_url FROM users WHERE user_id = ?',(str([id]),))
    return c.fetchone()

def get_count_money(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT money FROM users WHERE user_id = ?',(str([id]),))
    return c.fetchone()

def get_all(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?',(str([id]),))
    return c.fetchone()

def add_1_count_url(id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET count_url = ? WHERE user_id = ?', (str(1+int(get_count_url(id)[0])), str([id]),))
    conn.commit()

def update_money_plus(id,sum):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET money = ? WHERE user_id = ?', (str(sum+int(get_count_money(id)[0])), str([id]),))
    conn.commit()

def update_money_minus(id,minus):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET money = ? WHERE user_id = ?', (str(int(get_count_money(id)[0])-minus), str([id]),))
    conn.commit()

def add_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (user_id, count_url, money,total_money) VALUES (?,?,?,?)', (str([user_id]), '0', '0', '0',))
    conn.commit()