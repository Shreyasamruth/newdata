from flask import Blueprint, render_template, request, redirect, session, flash
from app.db import get_db, hash_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not login_input or not password:
            flash('Please enter both username/email and password.', 'danger')
            return render_template('login.html')

        pwd_hash = hash_password(password)

        conn = get_db()
        cursor = conn.cursor()
        
        # Support login via email OR username 'admin'
        cursor.execute('''
            SELECT * FROM users 
            WHERE (email = ? OR name = ?) AND password_hash = ?
        ''', (login_input, login_input, pwd_hash))
        
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            session['user_role'] = user['role']

            flash(f'Welcome back, {user["name"]}!', 'success')
            
            if user['role'] == 'admin':
                return redirect('/admin')
            return redirect('/')
        else:
            flash('Invalid credentials. Please check your username/email and password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('login.html', show_register=True)

        pwd_hash = hash_password(password)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            flash('An account with this email already exists.', 'danger')
            return render_template('login.html', show_register=True)

        cursor.execute('''
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, 'user')
        ''', (name, email, pwd_hash))
        conn.commit()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        new_user = cursor.fetchone()
        conn.close()

        session['user_id'] = new_user['id']
        session['user_email'] = new_user['email']
        session['user_name'] = new_user['name']
        session['user_role'] = new_user['role']

        flash('Account created successfully! Welcome to PSWX AI.', 'success')
        return redirect('/')

    return render_template('login.html', show_register=True)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/login')
