#models/user.py
def create_user_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            is_admin BOOLEAN DEFAULT FALSE
        )
    ''')
    create_user(cursor,'arvi', 'pass', 'admin@gmail.com', '1234567890', True)

def create_user(cursor, username, password, email, phone=None, is_admin=False):
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email, phone, is_admin)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, email, phone, is_admin))


def check_user_exists(cursor,username):
    cursor.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    return cursor.fetchone()
