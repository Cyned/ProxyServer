import os
from waitress import serve

from app import app, server


if __name__ == '__main__':
    serve(
        app,
        host=os.environ.get("HOST", "127.0.0.1"),
        port=os.environ.get("PORT", 9000),
        expose_tracebacks=True,
    )
