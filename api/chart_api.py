from flask import Blueprint, jsonify
import sqlite3

chart_bp = Blueprint('chart_bp', __name__)
DB_PATH = 'parking.db'

# 1. Spot Status Distribution
@chart_bp.route('/api/chart/spot-status')
def spot_status():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT status, COUNT(*) FROM parking_spots GROUP BY status
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"status": r[0], "count": r[1]} for r in rows])

# 2. Lot-wise Occupancy
@chart_bp.route('/api/chart/lot-occupancy')
def lot_occupancy():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT l.prime_location_name,
               SUM(CASE WHEN s.status = 'O' THEN 1 ELSE 0 END) AS occupied,
               COUNT(s.id) AS total
        FROM parking_lots l
        LEFT JOIN parking_spots s ON l.id = s.lot_id
        GROUP BY l.id
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"lot": r[0], "occupied": r[1], "total": r[2]} for r in rows])

# 3. Monthly Revenue
@chart_bp.route('/api/chart/monthly-revenue')
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

# 4. Top Users by Reservations
@chart_bp.route('/api/chart/top-users')
def top_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, COUNT(r.id) as count
        FROM users u
        JOIN reservations r ON u.user_id = r.user_id
        GROUP BY u.user_id
        ORDER BY count DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"username": r[0], "reservations": r[1]} for r in rows])

# 5. User Monthly Usage
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

