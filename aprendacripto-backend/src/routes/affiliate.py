from flask import Blueprint, request, jsonify, session
from src.models.content import AffiliateLink, db
from src.models.admin import LinkClick
from datetime import datetime

affiliate_bp = Blueprint('affiliate', __name__)

def require_auth():
    if 'admin_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    return None

@affiliate_bp.route('/links', methods=['GET'])
def get_affiliate_links():
    try:
        links = AffiliateLink.query.filter_by(is_active=True).all()
        return jsonify([link.to_dict() for link in links]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/links', methods=['GET'])
def get_admin_affiliate_links():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        links = AffiliateLink.query.order_by(AffiliateLink.created_at.desc()).all()
        return jsonify([link.to_dict() for link in links]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/links', methods=['POST'])
def create_affiliate_link():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        required_fields = ['name', 'url']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        link = AffiliateLink(
            name=data['name'],
            url=data['url'],
            description=data.get('description'),
            is_active=data.get('is_active', True)
        )

        db.session.add(link)
        db.session.commit()

        return jsonify(link.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/links/<int:link_id>', methods=['PUT'])
def update_affiliate_link(link_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        link = AffiliateLink.query.get(link_id)
        if not link:
            return jsonify({'error': 'Affiliate link not found'}), 404

        data = request.get_json()

        # Update fields
        if 'name' in data:
            link.name = data['name']
        if 'url' in data:
            link.url = data['url']
        if 'description' in data:
            link.description = data['description']
        if 'is_active' in data:
            link.is_active = data['is_active']

        link.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(link.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/admin/links/<int:link_id>', methods=['DELETE'])
def delete_affiliate_link(link_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        link = AffiliateLink.query.get(link_id)
        if not link:
            return jsonify({'error': 'Affiliate link not found'}), 404

        db.session.delete(link)
        db.session.commit()

        return jsonify({'message': 'Affiliate link deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@affiliate_bp.route('/click/<int:link_id>', methods=['POST'])
def track_click(link_id):
    try:
        link = AffiliateLink.query.get(link_id)
        if not link or not link.is_active:
            return jsonify({'error': 'Link not found or inactive'}), 404

        # Track the click
        click = LinkClick(
            affiliate_link_id=link_id,
            visitor_ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer')
        )

        db.session.add(click)
        db.session.commit()

        return jsonify({
            'message': 'Click tracked',
            'redirect_url': link.url
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

