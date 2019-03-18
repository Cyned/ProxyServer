import os
from waitress import serve

from flask_app.app import app
from app.server import proxy

if __name__ == '__main__':
    serve(app,
          host=os.environ.get("HOST", "127.0.0.1"),
          port=os.environ.get("PORT", 9000),
          expose_tracebacks=True)

# if __name__ == '__main__':
#    app.run(host='127.0.0.1', port=8081, debug=True)
