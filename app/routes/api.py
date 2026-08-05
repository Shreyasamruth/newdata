from flask import Blueprint, request, jsonify, send_file, session
from app.services.ml_engine import ml_engine
from app.services.entropy_calculator import estimate_crack_times, compute_health_score
from app.services.generator import generate_password
from app.services.report_generator import generate_pdf_report
from app.db import get_db, hash_password
import io

api_bp = Blueprint('api', __name__)

@api_bp.route('/analyze', methods=['POST'])
def analyze_password():
    data = request.get_json() or {}
    password = data.get('password', '')

    if not password:
        return jsonify({'error': 'Password input is required'}), 400

    # 1. ML Engine Inference
    ml_res = ml_engine.predict(password)
    features = ml_res['features']

    # 2. Entropy & Crack Time Estimation
    crack_times = estimate_crack_times(password)
    
    # 3. Password Health Score (0-100)
    health_score = compute_health_score(password, features)

    # 4. Generate Personalized Recommendations
    recommendations = []
    if len(password) < 12:
        recommendations.append(f"Increase password length from {len(password)} to at least 14+ characters.")
    if features.get('num_uppercase', 0) == 0:
        recommendations.append("Include uppercase letters (A-Z) to expand character pool size.")
    if features.get('num_symbols', 0) == 0:
        recommendations.append("Add special symbols (!@#$%^&*) to maximize entropy.")
    if features.get('dictionary_matches', 0) > 0:
        recommendations.append("Remove dictionary words or common names to prevent dictionary attacks.")
    if features.get('keyboard_pattern_score', 0) > 0:
        recommendations.append("Avoid QWERTY keyboard physical patterns (e.g. 'qwerty', 'asdfgh').")
    if features.get('sequential_chars', 0) > 0:
        recommendations.append("Avoid sequential sequences (e.g. 'abc', '123').")

    if not recommendations and health_score['score'] >= 80:
        recommendations.append("Password meets high cybersecurity standards. Excellent randomness and complexity!")

    # Mask password for privacy preview
    masked = password[0] + "*" * (len(password) - 2) + password[-1] if len(password) > 2 else "***"

    # 5. Automatically Collect and Store Analyzed Password in User Vault (Cryptographic Hash format)
    user_id = session.get('user_id')
    if user_id:
        try:
            pwd_hash = hash_password(password)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO saved_passwords 
                (user_id, password_hash, masked_password, health_score, category, entropy_bits)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, pwd_hash, masked, health_score['score'], health_score['category'], features['shannon_entropy']))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Vault Collection Error:", e)

    return jsonify({
        'status': 'success',
        'masked_password': masked,
        'length': len(password),
        'ml_prediction': {
            'predicted_class_id': ml_res['predicted_class_id'],
            'predicted_label': ml_res['predicted_label'],
            'confidence': ml_res['confidence'],
            'model_used': ml_res['model_used']
        },
        'health_score': health_score,
        'entropy_bits': features['shannon_entropy'],
        'crack_times': crack_times,
        'features': features,
        'recommendations': recommendations
    })

@api_bp.route('/generate', methods=['POST'])
def generate():
    data = request.get_json() or {}
    category = data.get('category', 'custom')
    length = int(data.get('length', 16))
    include_upper = bool(data.get('include_upper', True))
    include_digits = bool(data.get('include_digits', True))
    include_symbols = bool(data.get('include_symbols', True))

    pwd = generate_password(
        category=category,
        length=length,
        include_upper=include_upper,
        include_digits=include_digits,
        include_symbols=include_symbols
    )

    ml_res = ml_engine.predict(pwd)
    crack_times = estimate_crack_times(pwd)
    health_score = compute_health_score(pwd, ml_res['features'])

    return jsonify({
        'status': 'success',
        'generated_password': pwd,
        'length': len(pwd),
        'entropy_bits': ml_res['features']['shannon_entropy'],
        'health_score': health_score,
        'crack_times': crack_times,
        'predicted_label': ml_res['predicted_label']
    })

@api_bp.route('/export-pdf', methods=['POST'])
def export_pdf():
    data = request.get_json() or {}
    masked_password = data.get('masked_password', '***')
    health_score = data.get('health_score', {'score': 85, 'category': 'Strong', 'color': '#00cc66'})
    entropy_bits = data.get('entropy_bits', 72.5)
    crack_times = data.get('crack_times', {})
    recommendations = data.get('recommendations', [])

    pdf_bytes = generate_pdf_report(
        password_mask=masked_password,
        health_score=health_score,
        entropy=entropy_bits,
        crack_times=crack_times,
        recommendations=recommendations
    )

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name='Security_Audit_Report.pdf'
    )

@api_bp.route('/model-stats', methods=['GET'])
def model_stats():
    metrics = ml_engine.get_metrics()
    return jsonify(metrics if metrics else {'status': 'metrics_not_ready'})
