from flask import Blueprint, request, jsonify, session
from src.models.admin import Analytics, LinkClick, db
from src.models.content import AffiliateLink
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)

def require_auth():
    if 'admin_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    return None

@analytics_bp.route('/track', methods=['POST'])
def track_page_view():
    try:
        data = request.get_json()
        page_slug = data.get('page_slug', 'home')

        analytics = Analytics(
            page_slug=page_slug,
            visitor_ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            referrer=request.headers.get('Referer')
        )

        db.session.add(analytics)
        db.session.commit()

        return jsonify({'message': 'Page view tracked'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/admin/dashboard', methods=['GET'])
def get_dashboard_data():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        # Get date range (last 30 days by default)
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)

        # Total page views
        total_views = Analytics.query.filter(Analytics.timestamp >= start_date).count()

        # Page views by page
        page_views = db.session.query(
            Analytics.page_slug,
            func.count(Analytics.id).label('views')
        ).filter(Analytics.timestamp >= start_date).group_by(Analytics.page_slug).all()

        # Total link clicks
        total_clicks = LinkClick.query.filter(LinkClick.timestamp >= start_date).count()

        # Link clicks by affiliate link
        link_clicks = db.session.query(
            AffiliateLink.name,
            func.count(LinkClick.id).label('clicks')
        ).join(LinkClick, AffiliateLink.id == LinkClick.affiliate_link_id)\
         .filter(LinkClick.timestamp >= start_date)\
         .group_by(AffiliateLink.name).all()

        # Daily views for chart
        daily_views = db.session.query(
            func.date(Analytics.timestamp).label('date'),
            func.count(Analytics.id).label('views')
        ).filter(Analytics.timestamp >= start_date)\
         .group_by(func.date(Analytics.timestamp))\
         .order_by(func.date(Analytics.timestamp)).all()

        # Top referrers
        top_referrers = db.session.query(
            Analytics.referrer,
            func.count(Analytics.id).label('views')
        ).filter(Analytics.timestamp >= start_date)\
         .filter(Analytics.referrer.isnot(None))\
         .group_by(Analytics.referrer)\
         .order_by(func.count(Analytics.id).desc())\
         .limit(10).all()

        return jsonify({
            'total_views': total_views,
            'total_clicks': total_clicks,
            'page_views': [{'page': pv.page_slug, 'views': pv.views} for pv in page_views],
            'link_clicks': [{'link': lc.name, 'clicks': lc.clicks} for lc in link_clicks],
            'daily_views': [{'date': str(dv.date), 'views': dv.views} for dv in daily_views],
            'top_referrers': [{'referrer': tr.referrer, 'views': tr.views} for tr in top_referrers],
            'period_days': days
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/admin/export', methods=['GET'])
def export_analytics():
    auth_error = require_auth()
    if auth_error:
        return auth_error
    
    try:
        # Get date range
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)

        # Get all analytics data
        analytics_data = Analytics.query.filter(Analytics.timestamp >= start_date).all()
        clicks_data = LinkClick.query.filter(LinkClick.timestamp >= start_date).all()

        return jsonify({
            'analytics': [a.to_dict() for a in analytics_data],
            'clicks': [c.to_dict() for c in clicks_data],
            'exported_at': datetime.utcnow().isoformat(),
            'period_days': days
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

