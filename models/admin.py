#models/admin.py
def superadmin_create(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO admin (username, password)
        VALUES ('arvi', 'pass')
    ''')

def check_admin_exists(cursor, username):
    cursor.execute('''
        SELECT * FROM admin WHERE username = ?
    ''', (username,))
    return cursor.fetchone()