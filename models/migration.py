import sqlite3

DB_PATH = 'parking.db'

def remove_unique_constraint_vehicle_no():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Step 1: Rename old table
        cursor.execute("ALTER TABLE reservations RENAME TO old_reservations")

        # Step 2: Create new table without UNIQUE on vehicle_no
        cursor.execute("""
            CREATE TABLE reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spot_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                parking_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                leaving_timestamp TEXT,
                parking_cost REAL DEFAULT 0,
                vehicle_no TEXT NOT NULL,
                price_per_hour REAL NOT NULL,
                FOREIGN KEY (spot_id) REFERENCES parking_spots(id)
            )
        """)

        # Step 3: Copy data
        cursor.execute("""
            INSERT INTO reservations (
                id, spot_id, user_id, parking_timestamp,
                leaving_timestamp, parking_cost, vehicle_no, price_per_hour
            )
            SELECT id, spot_id, user_id, parking_timestamp,
                   leaving_timestamp, parking_cost, vehicle_no, price_per_hour
            FROM old_reservations
        """)

        # Step 4: Drop old table
        cursor.execute("DROP TABLE old_reservations")

        conn.commit()
        print("✅ UNIQUE constraint on vehicle_no removed successfully.")
    except Exception as e:
        print("❌ Error during migration:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    remove_unique_constraint_vehicle_no()
