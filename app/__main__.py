"""Entry point: python -m app"""
from flask import Flask

from .db import init_db
from .transfers import bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    init_db()
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000)
