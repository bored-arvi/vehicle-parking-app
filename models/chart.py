#models/chart.py
from flask import Blueprint, jsonify, request
import sqlite3

chart_bp = Blueprint('chart_bp', __name__)

DB_PATH = 'parking.db'

# ---------- UTIL FUNCTION ----------
def fetch_data(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- ADMIN APIs ----------

@chart_bp.route('/api/chart/utilization')
def get_utilization_per_lot():
    query = """
        SELECT 
            lot_id,
            SUM(CASE WHEN status = 'A' THEN 1 ELSE 0 END) AS available,
            SUM(CASE WHEN status = 'O' THEN 1 ELSE 0 END) AS occupied
        FROM spots
        GROUP BY lot_id;
    """
    rows = fetch_data(query)
    return jsonify([{'lot_id': r[0], 'available': r[1], 'occupied': r[2]} for r in rows])

@chart_bp.route('/api/chart/revenue')
def get_revenue_over_time():
    query = """
        SELECT 
            DATE(timestamp_out),
            SUM(total_cost)
        FROM reservations
        WHERE status = 'released'
        GROUP BY DATE(timestamp_out)
        ORDER BY DATE(timestamp_out);
    """
    rows = fetch_data(query)
    return jsonify([{'date': r[0], 'earnings': r[1]} for r in rows])

@chart_bp.route('/api/chart/active-lots')
def get_active_lots_by_reservations():
    query = """
        SELECT 
            s.lot_id,
            COUNT(r.id)
        FROM reservations r
        JOIN spots s ON r.spot_id = s.id
        GROUP BY s.lot_id
        ORDER BY COUNT(r.id) DESC;
    """
    rows = fetch_data(query)
    return jsonify([{'lot_id': r[0], 'reservations': r[1]} for r in rows])

@chart_bp.route('/api/chart/spot-distribution')
def get_spot_status_distribution():
    query = """
        SELECT 
            status,
            COUNT(*)
        FROM spots
        GROUP BY status;
    """
    rows = fetch_data(query)
    return jsonify([{'status': r[0], 'count': r[1]} for r in rows])

# ---------- USER APIs ----------

@chart_bp.route('/api/chart/user-timeline/<int:user_id>')
def get_user_reservations_timeline(user_id):
    query = """
        SELECT 
            DATE(timestamp_out),
            COUNT(*)
        FROM reservations
        WHERE user_id = ? AND status = 'released'
        GROUP BY DATE(timestamp_out)
        ORDER BY DATE(timestamp_out);
    """
    rows = fetch_data(query, (user_id,))
    return jsonify([{'date': r[0], 'count': r[1]} for r in rows])

@chart_bp.route('/api/chart/user-summary/<int:user_id>')
def get_user_cost_and_duration(user_id):
    query = """
        SELECT 
            SUM(total_cost),
            SUM((JULIANDAY(timestamp_out) - JULIANDAY(timestamp_in)) * 24 * 60)
        FROM reservations
        WHERE user_id = ? AND status = 'released';
    """
    rows = fetch_data(query, (user_id,))
    total_cost, total_minutes = rows[0]
    return jsonify({
        'total_spent': round(total_cost or 0, 2),
        'total_minutes': int(total_minutes or 0)
    })
