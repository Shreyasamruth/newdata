from flask import Blueprint, render_template, session, redirect, url_for
from app.db import get_db

vault_bp = Blueprint('vault', __name__)

@vault_bp.route('/vault')
def view_vault():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM saved_passwords 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,))
    
    passwords = cursor.fetchall()
    conn.close()

    return render_template('vault.html', passwords=passwords)
