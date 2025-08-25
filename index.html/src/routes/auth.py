from flask import Blueprint, request, jsonify, session
from src.models.admin import Admin, db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password) and admin.is_active:
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            
            # Update last login
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'message': 'Login successful',
                'admin': admin.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    try:
        if 'admin_id' in session:
            admin = Admin.query.get(session['admin_id'])
            if admin and admin.is_active:
                return jsonify({
                    'authenticated': True,
                    'admin': admin.to_dict()
                }), 200
        
        return jsonify({'authenticated': False}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    try:
        if 'admin_id' not in session:
            return jsonify({'error': 'Not authenticated'}), 401

        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'error': 'Current and new passwords are required'}), 400

        admin = Admin.query.get(session['admin_id'])
        if not admin or not admin.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400

        admin.set_password(new_password)
        db.session.commit()

        return jsonify({'message': 'Password changed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

