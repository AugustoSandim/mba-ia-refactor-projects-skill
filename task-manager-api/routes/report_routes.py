from flask import Blueprint, jsonify
from controllers import report_controller

report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    data, status = report_controller.summary_report()
    return jsonify(data), status

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    data, status = report_controller.user_report(user_id)
    return jsonify(data), status
