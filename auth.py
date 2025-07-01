from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from models import User
from functools import wraps

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['email'] = user['email']
            session['is_admin'] = user.get('is_admin', False)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if User.get_by_email(email):
            flash('Email already registered', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data = {
            'email': email,
            'password': hashed_password,
            'is_admin': False
        }
        
        if User.create(user_data):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('Error during registration', 'danger')
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out', 'success')
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    user = User.get_by_email(session['email'])
    return render_template('auth/profile.html', user=user)
