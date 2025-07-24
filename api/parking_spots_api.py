# controllers/parking_spots_api.py
from flask import Blueprint, request, jsonify
import sqlite3
from models.parking_spot import (
    add_parking_spot, delete_parking_spot,
    reserve_parking_spot, release_parking_spot,
    get_available_spots
)
from models.parking_lot import  add_parking_lot_spots,get_parking_lots 

parking_spot_bp = Blueprint('parking_spot_bp', __name__)

DB_NAME = 'parking.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@parking_spot_bp.route('/api/spot/add', methods=['POST'])
def api_add_spot():
    data = request.json
    lot_id = data.get('lot_id')
    if not lot_id:
        return jsonify({'error': 'lot_id is required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    add_parking_spot(cursor, lot_id)
    conn.commit()
    conn.close()
    return jsonify({'message': 'Parking spot added'}), 201

@parking_spot_bp.route('/api/spot/delete/<int:spot_id>', methods=['DELETE'])
def api_delete_spot(spot_id):
    conn = get_db()
    cursor = conn.cursor()
    delete_parking_spot(cursor, spot_id)
    conn.commit()
    conn.close()
    return jsonify({'message': f'Spot {spot_id} deleted'}), 200

@parking_spot_bp.route('/api/spot/reserve/<int:spot_id>', methods=['POST'])
def api_reserve_spot(spot_id):
    conn = get_db()
    cursor = conn.cursor()
    reserve_parking_spot(cursor, spot_id)
    conn.commit()
    conn.close()
    return jsonify({'message': f'Spot {spot_id} reserved'}), 200

@parking_spot_bp.route('/api/spot/release/<int:spot_id>', methods=['POST'])
def api_release_spot(spot_id):
    conn = get_db()
    cursor = conn.cursor()
    release_parking_spot(cursor, spot_id)
    conn.commit()
    conn.close()
    return jsonify({'message': f'Spot {spot_id} released'}), 200

@parking_spot_bp.route('/api/spot/available/<int:lot_id>', methods=['GET'])
def api_get_available_spots(lot_id):
    conn = get_db()
    cursor = conn.cursor()
    spots = get_available_spots(cursor, lot_id)
    conn.close()
    return jsonify([dict(spot) for spot in spots]), 200

@parking_spot_bp.route('/lot/spot/add', methods=['POST'])
def add_lot_with_spots():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    address = data.get('address')
    pincode = data.get('pincode')
    max_spots = data.get('max_spots')

    if not all([name, price, max_spots]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    add_parking_lot_spots(cursor, name, price, address, pincode, max_spots)
    conn.commit()
    conn.close()

    return jsonify({'message': 'Parking lot and spots added successfully'}), 201



@parking_spot_bp.route('/api/lots', methods=['GET'])
def api_get_parking_lots():
    conn = get_db()
    cursor = conn.cursor()
    lots = get_parking_lots(cursor)
    conn.close()
    return jsonify([dict(lot) for lot in lots]), 200
