"""
WSGI entry point for production deployment.

Usage:
  Linux/Mac (Gunicorn):
    gunicorn -w 1 --threads 4 -b 0.0.0.0:5000 wsgi:app

  Windows (Waitress):
    waitress-serve --host=0.0.0.0 --port=5000 --threads=4 wsgi:app

  Docker:
    See Dockerfile
"""
from app import app

if __name__ == '__main__':
    try:
        from waitress import serve
        print("Starting production server (Waitress) on 0.0.0.0:5000...")
        serve(app, host='0.0.0.0', port=5000, threads=4)
    except ImportError:
        print("Waitress not installed. Install with: pip install waitress")
        print("Falling back to Flask development server...")
        app.run(host='0.0.0.0', port=5000)
