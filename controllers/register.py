#controllers/register.py
from flask import flash, redirect, render_template, request, url_for # Replace with your DB name

from flask import Blueprint, render_template
from controllers import register_bp
DB_NAME = 'parking.db'
import sqlite3
@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone = request.form.get('phone', '')
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (name, username, email, phone, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, username, email, phone, password))
            conn.commit()
            return redirect('/auth/user')
        except sqlite3.IntegrityError:
            return "Username or Email already exists."
        finally:
            conn.close()
    return render_template('register.html')
