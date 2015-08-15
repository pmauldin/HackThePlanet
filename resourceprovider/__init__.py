import flask
from routes import add_routes_to
from flask_sslify import SSLify

# or, make your own!


def create_app(config):
    app = flask.Flask(__name__)
    app.config.update(config)
    add_routes_to(app)
    SSLify(app)
    return app

if __name__ == '__main__':
    app.run()
