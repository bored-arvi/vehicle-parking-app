#api/search_api.py
from flask import request, jsonify, Blueprint, request 
import sqlite3 # adjust if needed

search_bp = Blueprint('search_bp', __name__)

DB_NAME = 'parking.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

@search_bp.route('/api/search', methods=['GET'])
def search_lots_with_spots():
    location = request.args.get('location', '').strip()
    pincode = request.args.get('pincode', '').strip()
    availability_values = request.args.getlist('availability') 
    

    base_query = '''
        SELECT pl.id as lot_id, pl.prime_location_name, pl.pin_code, pl.price
        FROM parking_lots pl
        WHERE 1=1
    '''
    params = []

    if location:
        base_query += ' AND pl.prime_location_name LIKE ?'
        params.append(f"%{location}%")
    if pincode:
        base_query += ' AND pl.pin_code = ?'
        params.append(pincode)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(base_query, params)
        lots = cursor.fetchall()

        results = []
        for lot in lots:
            cursor.execute('''
                SELECT id, lot_id, status
                FROM parking_spots
                WHERE lot_id = ?
            ''', (lot['lot_id'],))
            spots = cursor.fetchall()

            # Filter spots by availability if any filter is selected
            if availability_values:
                filtered_spots = []
                if 'available' in availability_values:
                    filtered_spots += [s for s in spots if s['status'] == 'A']
                if 'occupied' in availability_values:
                    filtered_spots += [s for s in spots if s['status'] == 'O']
                if not filtered_spots:
                    continue
                spots = filtered_spots

            lot_data = dict(lot)
            lot_data['spots'] = [dict(s) for s in spots]
            lot_data['occupied_count'] = sum(1 for s in spots if s['status'] == 'O')
            lot_data['available_count'] = sum(1 for s in spots if s['status'] == 'A')
            lot_data['total_spots'] = len(spots)

            results.append(lot_data)

    return jsonify(results), 200

