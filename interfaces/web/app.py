from flask import Flask, jsonify
from flasgger import Swagger
from infrastructure.factories import DatabaseFactory
from .controllers import bp as controllers_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'Blog API',
        'version': '1.0',
        'description': 'Simple blog API with Clean Architecture',
    }

    Swagger(app, template={
        'info': {
            'title': 'Blog API',
            'version': '1.0',
            'description': 'Documentation for Blog API endpoints'
        }
    })
    
    DatabaseFactory.initialize_db(app)
    
    app.register_blueprint(controllers_bp)
    
    @app.route('/favicon.ico')
    def favicon():
        return '', 204

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.'
        }), 500
    
    return app