from src.models.user import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_slug = db.Column(db.String(100), nullable=False)
    visitor_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'page_slug': self.page_slug,
            'visitor_ip': self.visitor_ip,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class LinkClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    affiliate_link_id = db.Column(db.Integer, db.ForeignKey('affiliate_link.id'), nullable=False)
    visitor_ip = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    referrer = db.Column(db.String(500), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'affiliate_link_id': self.affiliate_link_id,
            'visitor_ip': self.visitor_ip,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

