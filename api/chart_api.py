from flask import Blueprint, jsonify, request
import sqlite3

chart_bp = Blueprint('chart_bp', __name__)
DB_PATH = 'parking.db'

@chart_bp.route('/api/chart/admin/spot-status')
def spot_status():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT status, COUNT(*) FROM parking_spots GROUP BY status
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"status": r[0], "count": r[1]} for r in rows])


@chart_bp.route('/api/chart/admin/monthly-revenue')
def monthly_revenue():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT strftime('%Y-%m', parking_timestamp) AS month, SUM(parking_cost)
        FROM reservations
        WHERE parking_cost IS NOT NULL
        GROUP BY month
        ORDER BY month
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"month": r[0], "revenue": r[1]} for r in rows])


@chart_bp.route('/api/chart/admin/lot-status')
def lot_status():
    lot_name = request.args.get('lot')
    if not lot_name:
        return jsonify({"error": "Missing lot name"}), 400
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT status, COUNT(*)
        FROM parking_spots ps
        JOIN parking_lots pl ON ps.lot_id = pl.id
        WHERE pl.prime_location_name = ?
        GROUP BY status
    """, (lot_name,))
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"status": r[0], "count": r[1]} for r in rows])


@chart_bp.route('/api/chart/admin/lot-daily-activity')
def lot_daily_activity():
    lot_name = request.args.get('lot')
    if not lot_name:
        return jsonify({"error": "Missing lot name"}), 400
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(r.parking_timestamp), COUNT(*)
        FROM reservations r
        JOIN parking_spots ps ON r.spot_id = ps.id
        JOIN parking_lots pl ON ps.lot_id = pl.id
        WHERE pl.prime_location_name = ? AND r.parking_timestamp >= DATE('now', '-30 days')
        GROUP BY DATE(r.parking_timestamp)
        ORDER BY DATE(r.parking_timestamp)
    """, (lot_name,))
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"date": r[0], "count": r[1]} for r in rows])


@chart_bp.route('/api/chart/admin/top-lots')
def top_lots():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT pl.prime_location_name, COUNT(*) as reservation_count
        FROM reservations r
        JOIN parking_spots ps ON r.spot_id = ps.id
        JOIN parking_lots pl ON ps.lot_id = pl.id
        GROUP BY pl.id
        ORDER BY reservation_count DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"lot": r[0], "count": r[1]} for r in rows])

# Helper: List all lot names for dropdown
@chart_bp.route('/api/chart/admin/lot-names')
def lot_names():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT prime_location_name FROM parking_lots")
    rows = cur.fetchall()
    conn.close()
    return jsonify([r[0] for r in rows])

@chart_bp.route('/api/chart/user-usage/<int:user_id>')
def user_usage(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT strftime('%Y-%m', parking_timestamp) AS month, COUNT(*)
        FROM reservations
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """, (user_id,))
    rows = cur.fetchall()
    print(rows)
    conn.close()
    return jsonify([{"month": r[0], "count": r[1]} for r in rows])

# 6. User Total Spent
@chart_bp.route('/api/chart/user-total/<int:user_id>')
def user_total(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(parking_cost) FROM reservations WHERE user_id = ?
    """, (user_id,))
    value = cur.fetchone()[0] or 0
    conn.close()
    return jsonify({"total_spent": value})

@chart_bp.route('/api/chart/user-frequent-lots/<int:user_id>')
def user_frequent_lots(user_id):
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pl.prime_location_name, COUNT(*) AS reservations
        FROM reservations r
        JOIN parking_spots ps ON r.spot_id = ps.id
        JOIN parking_lots pl ON ps.lot_id = pl.id
        WHERE r.user_id = ?
        GROUP BY pl.id
        ORDER BY reservations DESC
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"lot": row[0], "count": row[1]} for row in data])

@chart_bp.route('/api/chart/user-cost-line/<int:user_id>')
def user_cost_line(user_id):
    conn = sqlite3.connect('parking.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE(parking_timestamp) AS date, parking_cost
        FROM reservations
        WHERE user_id = ? AND parking_cost IS NOT NULL
        ORDER BY parking_timestamp
    """, (user_id,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"date": row[0], "cost": row[1]} for row in data])

