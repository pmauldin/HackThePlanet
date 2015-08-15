import flask
from resourceprovider.controllers import sso as ctrl

sso = flask.Blueprint('sso', __name__)
url = '/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>'


@sso.route('/subscriptions/<subscription_id>/cloudservices/<cloud_service_name>/resources/<resource_type>/<resource_name>/SsoToken', methods=['POST'])
def create_sso(subscription_id, cloud_service_name, resource_type, resource_name):
    try:
        token, timestamp = ctrl.create(
            subscription_id, cloud_service_name, resource_type, resource_name)
    except NotImplementedError as e:
        return flask.abort(500)
    else:
        return flask.render_template('sso.xml', token=token, timestamp=timestamp)


@sso.route('/sso', methods=['GET'])
def get_sso():
    args = dict(
        subscription_id=flask.request.args['subid'],
        cloud_service_name=flask.request.args['cloudservicename'],
        resource_type=flask.request.args['resourcetype'],
        resource_name=flask.request.args['resourcename'],
        token=flask.request.args['token'],
        timestamp=flask.request.args['timestamp']
    )
    if ctrl.get(**args):
        return 'Logged In'
    else:
        return flask.abort(404)
