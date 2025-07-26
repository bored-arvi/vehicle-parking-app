#models/reservations.py
import datetime
def create_reservations_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL ,
            parking_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            leaving_timestamp TEXT,
            parking_cost REAL DEFAULT 0,
            vehicle_no TEXT NOT NULL,
            price_per_hour REAL NOT NULL,
            FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
        )
    ''')

def add_reservation(cursor, spot_id, user_id, vehicle_no):
    cursor.execute('SELECT price FROM parking_spots WHERE id = ?', (spot_id,))
    price = cursor.fetchone()
    if price:
        price_per_hour = price[0]
    else:
        price_per_hour = 0  # Default price if not found
    cursor.execute('''
        INSERT INTO reservations (spot_id, user_id, vehicle_no, price_per_hour)
        VALUES (?, ?,?,?)
    ''', (spot_id, user_id,vehicle_no,price_per_hour))

def calculate_parking_cost(parking_timestamp,leaving_timestamp, price_per_hour):
    from datetime import datetime
    fmt = '%Y-%m-%d %H:%M:%S'
    start = datetime.strptime(parking_timestamp, fmt)
    end = datetime.strptime(leaving_timestamp, fmt)
    duration = (end - start).total_seconds() / 3600  # Convert seconds to hours
    return duration * price_per_hour

def get_reservations_by_user(cursor, user_id):
    cursor.execute('''
        SELECT * FROM reservations WHERE user_id = ?
    ''', (user_id,))
    return cursor.fetchall()

def get_parking_timestamp(cursor, reservation_id):
    cursor.execute('''
        SELECT parking_timestamp FROM reservations WHERE id = ?
    ''', (reservation_id,))
    return cursor.fetchone()[0]

def release_reservation(cursor, reservation_id,leaving_timestamp,parking_cost):
          
        cursor.execute('''
            UPDATE reservations
            SET leaving_timestamp = ?, parking_cost = ?
            WHERE id = ?
        ''', (leaving_timestamp, parking_cost, reservation_id))
        
        cursor.execute('''
            DELETE FROM reservations WHERE id = ?
        ''', (reservation_id,))

