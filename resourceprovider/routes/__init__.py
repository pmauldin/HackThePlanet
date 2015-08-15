from resources import resources
from subscriptions import subscriptions
from cloudservices import cloudservices
from sso import sso


def add_routes_to(app):
    for blueprint in [resources, subscriptions, cloudservices, sso]:
        app.register_blueprint(blueprint)
