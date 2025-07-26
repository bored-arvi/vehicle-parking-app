# api/reservations_api.py
from flask import Blueprint, request, jsonify
import sqlite3
from models.reservations import (
    add_reservation,
    calculate_parking_cost, get_reservations_by_user,
    get_parking_timestamp, release_reservation
)
import datetime

reservations_bp = Blueprint('reservations_bp', __name__)

DB_NAME = 'parking.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

@reservations_bp.route('/api/reservations/add', methods=['POST'])
def api_add_reservation():
    data = request.json
    user_id = data.get('user_id')
    spot_id = data.get('spot_id')
    vehicle_no = data.get('vehicle_number')

    if not all([user_id, spot_id, vehicle_no]):
        return jsonify({'error': 'All fields are required'}), 400

    with get_db() as conn:
        cursor = conn.cursor()
        add_reservation(cursor, spot_id, user_id, vehicle_no)
        conn.commit()

    return jsonify({'message': 'Reservation added successfully'}), 201

@reservations_bp.route('/api/reservations/cost', methods=['POST'])
def api_calculate_cost():  
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    price_per_hour = data.get('price_per_hour')

    if not all([start_time, end_time, price_per_hour]):
        return jsonify({'error': 'All fields are required'}), 400

    cost = calculate_parking_cost(start_time, end_time, price_per_hour)
    return jsonify({'cost': cost}), 200

@reservations_bp.route('/api/reservations/user/<int:user_id>', methods=['GET'])
def api_get_user_reservations(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        reservations = get_reservations_by_user(cursor, user_id)

    if not reservations:
        return jsonify({'message': 'No reservations found for this user'}), 404

    return jsonify([dict(reservation) for reservation in reservations]), 200

@reservations_bp.route('/api/reservations/release/<int:reservation_id>', methods=['POST'])
def api_release_reservation(reservation_id):
    with get_db() as conn:
        cursor = conn.cursor()

        reservation = get_parking_timestamp(cursor, reservation_id)
        if not reservation:
            return jsonify({'message': 'Reservation not found'}), 404

        leaving_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        parking_cost = calculate_parking_cost(reservation['parking_timestamp'], leaving_timestamp, reservation['price_per_hour'])

        release_reservation(cursor, reservation_id, leaving_timestamp, parking_cost)
        conn.commit()

    return jsonify({'message': 'Reservation released successfully', 'cost': parking_cost}), 200

@reservations_bp.route('/api/reservations/timestamp/<int:reservation_id>', methods=['GET'])
def api_get_parking_timestamp(reservation_id):
    with get_db() as conn:
        cursor = conn.cursor()
        parking_timestamp = get_parking_timestamp(cursor, reservation_id)

    if not parking_timestamp:
        return jsonify({'message': 'Reservation not found'}), 404

    return jsonify({'parking_timestamp': parking_timestamp}), 200