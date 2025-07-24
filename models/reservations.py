#models/reservations.py
def create_reservations_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            parking_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            leaving_timestamp TEXT,
            parking_cost REAL DEFAULT 0,
            FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
        )
    ''')

def add_reservation(cursor, spot_id, user_id):
    cursor.execute('''
        INSERT INTO reservations (spot_id, user_id)
        VALUES (?, ?)
    ''', (spot_id, user_id))

def update_reservation(cursor, reservation_id, leaving_timestamp):
    parking_cost=calculate_parking_cost(cursor, leaving_timestamp, reservation_id)
    cursor.execute('''
        UPDATE reservations
        SET leaving_timestamp = ?, parking_cost = ?
        WHERE id = ?
    ''', (leaving_timestamp, parking_cost, reservation_id))

def calculate_parking_cost(cursor,leaving_timestamp, parking_timestamp, price_per_hour):
    from datetime import datetime
    fmt = '%Y-%m-%d %H:%M:%S'
    start = datetime.strptime(parking_timestamp, fmt)
    end = datetime.strptime(leaving_timestamp, fmt)
    duration = (end - start).total_seconds() / 3600  # Convert seconds to hours
    return duration * price_per_hour
