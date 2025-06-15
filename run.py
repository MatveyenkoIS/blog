from interfaces.web.app import create_app
import signal
import sys

app = create_app()


def shutdown_handler(signum, frame):
    """Обработчик сигналов завершения работы."""
    print("\nЗавершение работы сервера...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    print("=" * 50)
    print("Запуск сервера Blog API")
    print("=" * 50)
    print("\nДокументация Swagger:")
    print("  GET  /apidocs/       - Интерактивная документация API")
    print("  GET  /apispec_1.json - Спецификация OpenAPI")
    print("\nБаза данных:")
    print(f"  SQLite: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("\n" + "=" * 50)
    print("Сервер запущен на http://localhost:5000")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        shutdown_handler(None, None)
    except Exception as e:
        print(f"\nОшибка: {str(e)}")
        sys.exit(1)