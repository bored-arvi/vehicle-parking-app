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
