from flask import render_template, session, request, redirect, url_for, g, flash
import sqlite3  # Replace with your actual blueprint
from controllers import auth_bp
DATABASE = 'parking.db'  # Replace with your DB name

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@auth_bp.teardown_app_request
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@auth_bp.route('/dashboard')
def dashboard():
    if 'role' in session and session['role'] == 'admin':
        db = get_db()
        lots = db.execute('SELECT * FROM parking_lots').fetchall()
        return render_template('admin_dash.html', lots=lots)
    else:
        return "Error: Unauthorized access", 403

@auth_bp.route('/lot/add', methods=['POST'])
def add_lot():
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    name = request.form['name']
    price = request.form['price']
    address = request.form['address']
    pincode = request.form['pincode']
    max_spots = request.form['max_spots']

    db = get_db()
    db.execute('INSERT INTO parking_lots (prime_location_name, price, address, pin_code, max_spots) VALUES (?, ?, ?, ?, ?)',
               (name, price, address, pincode, max_spots))
    db.commit()
    flash("Parking lot added successfully.")
    return redirect(url_for('auth_bp.dashboard'))

@auth_bp.route('/lot/edit/<int:lot_id>', methods=['POST'])
def edit_lot(lot_id):
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    name = request.form['name']
    price = request.form['price']
    address = request.form['address']
    pincode = request.form['pincode']
    max_spots = request.form['max_spots']

    db = get_db()
    db.execute('''UPDATE parking_lots SET prime_location_name=?, price=?, address=?, pin_code=?, max_spots=? WHERE id=?''',
               (name, price, address, pincode, max_spots, lot_id))
    db.commit()
    flash("Parking lot updated successfully.")
    return redirect(url_for('auth_bp.dashboard'))

@auth_bp.route('/lot/delete/<int:lot_id>', methods=['POST'])
def delete_lot(lot_id):
    if session.get('role') != 'admin':
        return "Unauthorized", 403

    db = get_db()
    spots = db.execute('SELECT COUNT(*) AS count FROM parking_spots WHERE lot_id=? AND status="O"', (lot_id,)).fetchone()

    if spots['count'] > 0:
        flash("Cannot delete: Spots in this lot are still occupied.")
        return redirect(url_for('auth_bp.dashboard'))

    db.execute('DELETE FROM parking_spots WHERE lot_id=?', (lot_id,))
    db.execute('DELETE FROM parking_lots WHERE id=?', (lot_id,))
    db.commit()
    flash("Parking lot deleted successfully.")
    return redirect(url_for('auth_bp.dashboard'))
