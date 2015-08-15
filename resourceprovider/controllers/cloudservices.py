"""
TODO: what are the cloudservice controllers?
"""
from resourceprovider.models import CloudService


def get(subscription_id, cloud_service_name):
    """
    This happens when a user views details about a purchased Cloud Service.
    """
    cs = CloudService()
    return cs.get(subscription_id, cloud_service_name)
