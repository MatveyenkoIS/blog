from interfaces.web.app import create_app
import signal
import sys

app = create_app()

def shutdown_handler(signum, frame):
    """Обработчик сигналов завершения работы"""
    print("\nShutting down server...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)
    
    print("=" * 50)
    print("Starting Blog API server")
    print("=" * 50)
    print("\nAvailable endpoints:")
    print("  GET  /               - API information")
    print("  POST /users          - Create user")
    print("  POST /posts          - Create post")
    print("  GET  /posts/<int:id> - Get post by ID")
    print("  POST /comments       - Create comment")
    print("\nSwagger Documentation:")
    print("  GET  /apidocs/       - Interactive API documentation")
    print("  GET  /apispec_1.json - OpenAPI specification")
    print("\nDatabase:")
    print(f"  SQLite: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("\n" + "=" * 50)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        shutdown_handler(None, None)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)