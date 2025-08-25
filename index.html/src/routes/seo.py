from flask import Blueprint, request, jsonify, session
from src.models.content import SeoConfig, db
from datetime import datetime

seo_bp = Blueprint('seo', __name__)

def require_auth():
    if 'admin_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    return None

@seo_bp.route('/config/<slug>', methods=['GET'])
def get_seo_config(slug):
    try:
        config = SeoConfig.query.filter_by(page_slug=slug).first()
        if not config:
            return jsonify({'error': 'SEO config not found'}), 404
        return jsonify(config.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seo_bp.route('/admin/config', methods=['GET'])
def get_admin_seo_configs():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        configs = SeoConfig.query.order_by(SeoConfig.created_at.desc()).all()
        return jsonify([config.to_dict() for config in configs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seo_bp.route('/admin/config', methods=['POST'])
def create_seo_config():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        required_fields = ['page_slug', 'title', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if config for this slug already exists
        existing_config = SeoConfig.query.filter_by(page_slug=data['page_slug']).first()
        if existing_config:
            return jsonify({'error': 'SEO config for this page already exists'}), 400

        config = SeoConfig(
            page_slug=data['page_slug'],
            title=data['title'],
            description=data['description'],
            keywords=data.get('keywords'),
            og_image=data.get('og_image')
        )

        db.session.add(config)
        db.session.commit()

        return jsonify(config.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seo_bp.route('/admin/config/<int:config_id>', methods=['PUT'])
def update_seo_config(config_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        config = SeoConfig.query.get(config_id)
        if not config:
            return jsonify({'error': 'SEO config not found'}), 404

        data = request.get_json()

        # Check if page_slug is being changed and if it already exists
        if data.get('page_slug') and data['page_slug'] != config.page_slug:
            existing_config = SeoConfig.query.filter_by(page_slug=data['page_slug']).first()
            if existing_config:
                return jsonify({'error': 'SEO config for this page already exists'}), 400

        # Update fields
        if 'page_slug' in data:
            config.page_slug = data['page_slug']
        if 'title' in data:
            config.title = data['title']
        if 'description' in data:
            config.description = data['description']
        if 'keywords' in data:
            config.keywords = data['keywords']
        if 'og_image' in data:
            config.og_image = data['og_image']

        config.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(config.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seo_bp.route('/admin/config/<int:config_id>', methods=['DELETE'])
def delete_seo_config(config_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        config = SeoConfig.query.get(config_id)
        if not config:
            return jsonify({'error': 'SEO config not found'}), 404

        db.session.delete(config)
        db.session.commit()

        return jsonify({'message': 'SEO config deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

