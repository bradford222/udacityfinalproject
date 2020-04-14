import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, DataProvider, Dataset

app = Flask(__name__)
setup_db(app)
CORS(app)

setup_db(app)

# ROUTES

@app.route('/providers', methods=['GET'])
def list_providers():
    providers = DataProvider.query.all()
    providers_formatted = [provider.short() for provider in providers]

    if len(providers) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'providers': providers_formatted
    })

# Error Handling

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

if __name__ == '__main__':
    app.run()