import flask
import xmltodict
from resourceprovider.controllers import cloudservices as ctrl

cloudservices = flask.Blueprint('cloudservices', __name__)
url = '/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>'


@cloudservices.route(url, methods=['GET'])
def get_cloudservice(subscription_id, cloud_service_name):
    try:
        result = ctrl.get(subscription_id, cloud_service_name)
    except NotImplementedError as e:
        return flask.abort(500)
    except LookupError as e:
        return flask.abort(404)
    else:
        return flask.render_template('cloudservice.xml', **result)
