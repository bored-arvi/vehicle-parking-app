#models/parking_spot.py
def create_parking_spot_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('A', 'O')) DEFAULT 'A',
            price REAL,
            FOREIGN KEY (lot_id) REFERENCES parking_lots(id)
        )
    ''')

def add_parking_spot(cursor, lot_id, status='A'):
    cursor.execute('SELECT price FROM parking_lots WHERE id = ?', (lot_id,));
    price = cursor.fetchone()
    if price:
        price = price[0]
    else:
        price = 0  # Default price if not found
    cursor.execute('''
        INSERT INTO parking_spots (lot_id, status,price)
        VALUES (?, ?,?)
    ''', (lot_id, status,price))

def get_available_spots(cursor, lot_id):
    cursor.execute('''
        SELECT * FROM parking_spots WHERE lot_id = ? AND status = 'A'
    ''', (lot_id,))
    return cursor.fetchall()

def delete_parking_spot(cursor, spot_id):
    cursor.execute('''
        DELETE FROM parking_spots WHERE id = ?
    ''', (spot_id,))

def reserve_parking_spot(cursor, spot_id):
    cursor.execute('''
        UPDATE parking_spots SET status = 'O' WHERE id = ?
    ''', (spot_id,))

def release_parking_spot(cursor, spot_id):
    cursor.execute('''
        UPDATE parking_spots SET status = 'A' WHERE id = ?
    ''', (spot_id,))

def add_multiple_spots(cursor, lot_id, count):
    for _ in range(count):
        add_parking_spot(cursor, lot_id)

def get_multiple_parking_status(cursor,lot_id):
    cursor.execute('''
            SELECT id,status from parking_spots WHERE lot_id = ?
        ''', (lot_id,))
    return cursor.fetchall()

def get_total_spots(cursor, lot_id):
    cursor.execute('''
        SELECT count(*) FROM parking_spots WHERE lot_id = ?
    ''', (lot_id,))
    return cursor.fetchone()[0]
