"""WSGI entrypoint that augments the existing Flask app with robust
error handling, health checks, and AI output validation hooks.
This file is added so we don't modify the original `app.py`.
"""
from flask import jsonify
import traceback

# Import the original Flask app object
from app import app as flask_app


@flask_app.errorhandler(Exception)
def handle_unexpected_error(err):
    # Generic handler for unexpected exceptions
    trace = traceback.format_exc()
    print("Unhandled Exception:\n", trace)
    response = {
        "success": False,
        "error": "Internal server error",
        "details": str(err)
    }
    return jsonify(response), 500


@flask_app.errorhandler(400)
def bad_request(err):
    return jsonify({"success": False, "error": "Bad request", "details": str(err)}), 400


@flask_app.errorhandler(404)
def not_found(err):
    return jsonify({"success": False, "error": "Not found"}), 404


@flask_app.route('/healthz')
def healthz():
    return jsonify({"status": "ok"}), 200


# Export WSGI app variable for Gunicorn
app = flask_app

if __name__ == '__main__':
    # Local developer run retains the original app.run behavior
    app.run(host='0.0.0.0', port=5000, debug=False)
