from flask import Flask, jsonify
from flasgger import Swagger
from infrastructure.factories import DatabaseFactory
from .controllers import bp as controllers_bp


def create_app() -> Flask:
    """
    Создать и настроить Flask приложение.
    
    Returns:
        Экземпляр Flask приложения
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SWAGGER'] = {
        'title': 'Blog API',
        'version': '1.0',
        'description': 'Простое API для блога с чистой архитектурой',
    }

    Swagger(app, template={
        'info': {
            'title': 'Blog API',
            'version': '1.0',
            'description': 'Документация для API блога'
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
            'error': 'Не найдено',
            'message': 'Запрашиваемый URL не найден на сервере.'
        }), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Внутренняя ошибка сервера',
            'message': 'Произошла непредвиденная ошибка.'
        }), 500
    
    return app