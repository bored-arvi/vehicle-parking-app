from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from models.user import check_user_exists
from models.admin import check_admin_exists
from controllers import auth_bp

@auth_bp.route('/admin', methods=['GET', 'POST'],endpoint='admin_login')

def admin_login():

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

@auth_bp.route('/user', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()

        if check_user_exists(cursor, username):
            session['role'] = 'user'
            session['username'] = username
            session['user_id'] = check_user_exists(cursor, username)[0]
            return redirect('/user/dashboard')
        else:
            return "Invalid credentials", 401
    return render_template("user.html")

@auth_bp.route('/user/charts',methods=['GET'])
def charts():
    return render_template('user_chart.html')
@auth_bp.route('/admin/charts',methods=['GET'])
def admin_charts():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_chart.html')
    else:
        return "Unauthorized", 403