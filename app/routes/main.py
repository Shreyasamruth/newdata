from flask import Blueprint, render_template, session, redirect, flash

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

@main_bp.route('/model-comparison')
def model_comparison():
    if 'user_id' not in session:
        return redirect('/login')

    # Restrict ML Model Analytics View to Administrators ONLY
    if session.get('user_role') != 'admin':
        flash('ML Model Analytics is restricted to Administrator access.', 'warning')
        return redirect('/')

    return render_template('model_comparison.html')
