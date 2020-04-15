import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, DataProvider, Dataset

def create_app():
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

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

    @app.route('/providers/<int:provider_id>', methods=['GET'])
    def provider_details(provider_id):
        provider = DataProvider.query.filter(DataProvider.id == provider_id).one_or_none()
        
        if provider is None:
            abort(404)

        return jsonify({
            'success': True,
            'provider': provider.long()
        })

    @app.route('/providers/<int:provider_id>', methods=['DELETE'])
    def delete_provider(provider_id):
        try:
            provider = DataProvider.query.filter(DataProvider.id == provider_id)\
                                    .one_or_none()

            if provider is None:
                abort(404)

            provider.delete()

            return jsonify({
                'success': True,
                'deleted': provider_id
            })

        except:
            abort(422)

    @app.route('/providers/<int:provider_id>', methods=['PATCH'])
    def update_provider_details(provider_id):
        provider = DataProvider.query.filter(DataProvider.id == provider_id).one_or_none()

        body = request.get_json()
        
        if provider is None:
            abort(404)

        name = body.get('name')
        description = body.get('description')
        biases = body.get('biases')
        try:
            provider.name = name
            provider.description = description
            provider.biases = biases
            provider.update()
            
            return jsonify({
                'success': True,
                'provider_id': provider.id
            })
        except:
            abort(422)

    @app.route('/providers', methods=['POST'])
    def add_provider():
        body = request.get_json()

        name = body.get('name')
        description = body.get('description')
        biases = body.get('biases')

        try:
            provider = DataProvider(name, description, biases)
            provider.insert()
            
            return jsonify({
                'success': True,
                'provider_id': provider.id
            })
        except:
            abort(422)

    @app.route('/datasets', methods=['POST'])
    def add_dataset():
        body = request.get_json()

        name = body.get('name')
        type = body.get('type')
        description = body.get('description')
        provider_id = body.get('provider_id')

        try:
            dataset = Dataset(name, provider_id, type, description)
            dataset.insert()
            
            return jsonify({
                'success': True,
                'provider_id': dataset.id
            })
        except Exception as es:
            print(es)
            abort(422)

    # Error Handling

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 400

    return app