#controllers/dash.py
from flask import render_template, session  # Replace with your DB name

from flask import Blueprint, render_template, session
from controllers import dashboard_bp

@dashboard_bp.route('/admin',methods=['GET','POST'])
def dashboard():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_dash.html')
    else:
        return "Unauthorized", 403
@dashboard_bp.route('/user', methods=['GET','POST'])
def user_dashboard():
    if 'role' in session and session['role'] == 'user':
        return render_template('user_dash.html')
    else:
        return "Unauthorized", 403

@dashboard_bp.route('/admin/users', methods=['GET'])
def admin_users():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_users.html')
    else:
        return "Unauthorized", 403

@dashboard_bp.route('/admin/search', methods=['GET'])
def search_lots():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_search.html')
    else:
        return "Unauthorized", 403

@dashboard_bp.route('/admin/charts',methods=['GET'])
def create_charts():
    if 'role' in session and session['role'] == 'admin':
        return render_template('admin_chart.html')
    else:
        return "Unauthorized", 403
@dashboard_bp.route('/user/charts',methods=['GET'])
def user_charts():  
    if 'role' in session and session['role'] == 'user':
        return render_template('user_chart.html')
    else:
        return "Unauthorized", 403
@dashboard_bp.route('user/reservations', methods=['GET'])
def user_reservations():
    if 'role' in session and session['role'] == 'user':
        return render_template('user_reservations.html')
    else:
        return "Unauthorized", 403
    

