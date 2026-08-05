from flask import Blueprint, render_template, session, redirect, flash
from app.db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    # 1. Enforce Admin Role Check
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('user_role') != 'admin':
        flash('Access Denied! Administrator privileges required.', 'danger')
        return redirect('/')

    conn = get_db()
    cursor = conn.cursor()

    # 2. Key Telemetry Metrics
    cursor.execute('SELECT COUNT(*) as total_users FROM users')
    total_users = cursor.fetchone()['total_users']

    cursor.execute('SELECT COUNT(*) as total_passwords FROM saved_passwords')
    total_passwords = cursor.fetchone()['total_passwords']

    cursor.execute('SELECT AVG(health_score) as avg_score FROM saved_passwords')
    avg_row = cursor.fetchone()
    avg_score = round(avg_row['avg_score'], 1) if avg_row and avg_row['avg_score'] else 0.0

    cursor.execute("SELECT COUNT(*) as weak_count FROM saved_passwords WHERE category = 'Weak'")
    weak_count = cursor.fetchone()['weak_count']

    # 3. User Directory
    cursor.execute('SELECT id, email, name, role, created_at FROM users ORDER BY created_at DESC')
    users_list = cursor.fetchall()

    # 4. Hashed Password Audit Logs (Cryptographic Hash Only for Admin Privacy View)
    cursor.execute('''
        SELECT sp.id, u.email, sp.password_hash, sp.health_score, sp.category, sp.entropy_bits, sp.created_at
        FROM saved_passwords sp
        JOIN users u ON sp.user_id = u.id
        ORDER BY sp.created_at DESC
        LIMIT 50
    ''')
    hashed_audit_logs = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        total_users=total_users,
        total_passwords=total_passwords,
        avg_score=avg_score,
        weak_count=weak_count,
        users_list=users_list,
        audit_logs=hashed_audit_logs
    )
