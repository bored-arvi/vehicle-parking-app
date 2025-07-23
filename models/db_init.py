#models/db_init.py
import sqlite3
from models.parking_lot import create_parking_lot_table
from models.parking_spot import create_parking_spot_table
from models.reservations import create_reservations_table
from models.user import create_user_table
from models.admin import superadmin_create

def init_db():
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()

    create_parking_lot_table(cursor)
    create_parking_spot_table(cursor)
    create_reservations_table(cursor)
    create_user_table(cursor)
    superadmin_create(cursor)

    conn.commit()
    conn.close()

