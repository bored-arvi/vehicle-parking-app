#models/parking_lot.py
from models.parking_spot import add_multiple_spots
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

def add_parking_lot_spots(cursor, name, price, address, pincode, max_spots):
    cursor.execute('''
        INSERT INTO parking_lots (prime_location_name, price, address, pin_code, max_spots)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, price, address, pincode, max_spots))
    cursor.execute('SELECT id from parking_lots WHERE prime_location_name = ? AND pin_code=?', (name,pincode))
    lot_id = cursor.fetchone()[0]
    add_multiple_spots(cursor, lot_id, max_spots)

def get_parking_lots(cursor):
    cursor.execute('''
        SELECT * FROM parking_lots
    ''')
    return cursor.fetchall()
