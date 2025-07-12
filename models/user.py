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

def create_user(cursor, username, password, email, phone=None, is_admin=False):
    cursor.execute('''
        INSERT INTO users (username, password, email, phone, is_admin)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, email, phone, is_admin))