from flask import Blueprint, request, jsonify, session
from src.models.content import Article, db
from datetime import datetime

content_bp = Blueprint('content', __name__)

def require_auth():
    if 'admin_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    return None

@content_bp.route('/articles', methods=['GET'])
def get_articles():
    try:
        articles = Article.query.filter_by(is_published=True).order_by(Article.created_at.desc()).all()
        return jsonify([article.to_dict() for article in articles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/articles/<slug>', methods=['GET'])
def get_article(slug):
    try:
        article = Article.query.filter_by(slug=slug, is_published=True).first()
        if not article:
            return jsonify({'error': 'Article not found'}), 404
        return jsonify(article.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/admin/articles', methods=['GET'])
def get_admin_articles():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        articles = Article.query.order_by(Article.created_at.desc()).all()
        return jsonify([article.to_dict() for article in articles]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/admin/articles', methods=['POST'])
def create_article():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        required_fields = ['title', 'content', 'slug']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Check if slug already exists
        existing_article = Article.query.filter_by(slug=data['slug']).first()
        if existing_article:
            return jsonify({'error': 'Article with this slug already exists'}), 400

        article = Article(
            title=data['title'],
            subtitle=data.get('subtitle'),
            content=data['content'],
            slug=data['slug'],
            read_time=data.get('read_time'),
            icon_name=data.get('icon_name'),
            color_gradient=data.get('color_gradient'),
            is_published=data.get('is_published', True)
        )

        db.session.add(article)
        db.session.commit()

        return jsonify(article.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/admin/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404

        data = request.get_json()

        # Check if slug is being changed and if it already exists
        if data.get('slug') and data['slug'] != article.slug:
            existing_article = Article.query.filter_by(slug=data['slug']).first()
            if existing_article:
                return jsonify({'error': 'Article with this slug already exists'}), 400

        # Update fields
        if 'title' in data:
            article.title = data['title']
        if 'subtitle' in data:
            article.subtitle = data['subtitle']
        if 'content' in data:
            article.content = data['content']
        if 'slug' in data:
            article.slug = data['slug']
        if 'read_time' in data:
            article.read_time = data['read_time']
        if 'icon_name' in data:
            article.icon_name = data['icon_name']
        if 'color_gradient' in data:
            article.color_gradient = data['color_gradient']
        if 'is_published' in data:
            article.is_published = data['is_published']

        article.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify(article.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@content_bp.route('/admin/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': 'Article not found'}), 404

        db.session.delete(article)
        db.session.commit()

        return jsonify({'message': 'Article deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

