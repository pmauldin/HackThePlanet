"""
TODO: what are the sso controllers?
"""
import hashlib
import flask
from datetime import datetime
import iso8601


def create(subscription_id, cloud_service_name, resource_type, resource_name):
    """
    Generates an SSO token and a timestamp indicating its freshness.
    """
    sso_secret = flask.current_app.config['SECRET_KEY']
    signature = "%s:%s:%s:%s:%s" % (
        subscription_id, cloud_service_name, resource_type, resource_name, sso_secret)
    return hashlib.sha256(signature).hexdigest(), datetime.now()


def get(subscription_id, cloud_service_name, resource_type, resource_name, token, timestamp):
    """
    Return a boolean indicating whether the given token is still valid, by two measures:
    1. Does it match our SSO secret?
    2. Is it younger than ten minutes?
    """
    local_token, local_timestamp = create(
        subscription_id, cloud_service_name, resource_type, resource_name)
    # do the tokens match?
    if local_token == token:
        remote_timestamp = iso8601.parse_date(timestamp).replace(tzinfo=None)
        # is the token recent enough?
        if (local_timestamp - remote_timestamp).seconds < 60 * 10:
            return True
        else:
            return False
    else:
        return False
