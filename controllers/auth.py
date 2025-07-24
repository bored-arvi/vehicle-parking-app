from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from models.user import check_user_exists
from models.admin import check_admin_exists
from controllers import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':
        username = request.form['admin_id']
        password = request.form['password']
        
        conn= sqlite3.connect('parking.db')
        cursor = conn.cursor()

        check= check_admin_exists(cursor, username)
        if check != None:
            if check[1] == password:
                session['role'] = 'admin'
                session['username'] = username
                return redirect('/admin/dashboard')
            else:
                return "Invalid password", 401
    return render_template("admin.html")
    
    
