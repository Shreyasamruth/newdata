from flask import Flask
from app.db import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pswx-cyber-security-ai-analyzer-secret-2026'

    # Initialize SQLite Database Tables & Default Accounts
    init_db()

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp
    from app.routes.vault import vault_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)
    app.register_blueprint(admin_bp)

    return app
