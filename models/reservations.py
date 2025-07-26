#models/reservations.py
import datetime
def create_reservations_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            parking_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            leaving_timestamp TEXT,
            parking_cost REAL DEFAULT 0,
            vehicle_no TEXT NOT NULL,
            FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
        )
    ''')

def add_reservation(cursor, spot_id, user_id, vehicle_no):
    cursor.execute('''
        INSERT INTO reservations (spot_id, user_id, vehicle_no)
        VALUES (?, ?,?)
    ''', (spot_id, user_id,vehicle_no))

def calculate_parking_cost(cursor,leaving_timestamp, parking_timestamp, price_per_hour):
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

def release_reservation(cursor, reservation_id):
    cursor.execute('''
        SELECT parking_timestamp,price_per_hour FROM reservations 
        JOIN parking_spots ON reservations.spot_id = parking_spots.id
        WHERE reservations.id = ?''', (reservation_id,))
    reservation= cursor.fetchone()
    if reservation:
        parking_timestamp, price_per_hour = reservation
        leaving_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        parking_cost = calculate_parking_cost(cursor, leaving_timestamp, parking_timestamp, price_per_hour)
        
        cursor.execute('''
            UPDATE reservations
            SET leaving_timestamp = ?, parking_cost = ?
            WHERE id = ?
        ''', (leaving_timestamp, parking_cost, reservation_id))
        
        cursor.execute('''
            DELETE FROM reservations WHERE id = ?
        ''', (reservation_id,))

