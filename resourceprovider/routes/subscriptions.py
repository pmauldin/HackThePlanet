import flask
import flask.views
from flask import request
import xmltodict
from resourceprovider.controllers import subscriptions as ctrl

subscriptions = flask.Blueprint('subscriptions', __name__)

events = {
    'Registered':   ctrl.registered,
    'Disabled':   ctrl.disabled,
    'Enabled':   ctrl.enabled,
    'Deleted':   ctrl.deleted
}


@subscriptions.route('/subscriptions/<subscription_id>/Events', methods=['POST'])
def subscribe(subscription_id):
    """
    handle subscription events: Registered, Disabled, Enabled, Deleted
    """
    body = xmltodict.parse(request.data)
    event = body['EntityEvent']['EntityState']
    if event in events.keys():
        try:
            result = events[event](subscription_id, body)
        except NotImplementedError:
            return flask.abort(500)
        else:
            return 200
    else:
        return flask.abort(400)
