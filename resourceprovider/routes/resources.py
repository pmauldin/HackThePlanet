import flask
from flask import request
import xmltodict
from resourceprovider.controllers import resources as ctrl

resources = flask.Blueprint('resources', __name__)
url = '/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>'

methods = {
    'GET': ctrl.get,
    'POST': ctrl.upgrade,
    'PUT': ctrl.create,
    'DELETE': ctrl.delete
}


@resources.route(url, methods=['GET', 'POST', 'PUT', 'DELETE'])
def resource(*args, **kwargs):
    body = xmltodict.parse(request.data)
    kwargs['body'] = body
    try:
        result = methods[request.method](*args, **kwargs)
    except NotImplementedError:
        return flask.abort(500)
    else:
        return flask.render_template('resource.xml', **result)
