#models/parking_lot.py
def create_parking_lot_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prime_location_name TEXT NOT NULL,
            price REAL NOT NULL,
            address TEXT,
            pin_code TEXT,
            max_spots INTEGER NOT NULL
        )
    ''')
