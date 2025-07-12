#models/parking_spot.py
def create_parking_spot_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parking_spots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lot_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('A', 'O')) DEFAULT 'A',
            FOREIGN KEY (lot_id) REFERENCES parking_lots(id)
        )
    ''')
