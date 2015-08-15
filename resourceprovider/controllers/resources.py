"""
TODO: what are the resource controllers?
"""
from resourceprovider.models import Resource


def create(subscription_id, cloud_service_name, resource_type, resource_name, body):
    """
    This happens when a user purchases your offering from the Windows Azure Store.
    """
    body.update({
        'subscription_id': subscription_id,
        'cloud_service_name': cloud_service_name,
        'resource_type': resource_type,
        'resource_name': resource_name
    })
    resource = Resource(**body)
    return resource.save()


def get(subscription_id, cloud_service_name, resource_type, resource_name, body):
    """
    This happens when a user views details about a purchased Resource.
    """
    return Resource().get(subscription_id, resource_type, resource_name)


def delete(subscription_id, cloud_service_name, resource_type, resource_name, body):
    """
    This happens when a user deletes a previously-purchased Resource.
    """
    return Resource().get(subscription_id, cloud_service_name, resource_type, resource_name).delete()


def upgrade(subscription_id, cloud_service_name, resource_type, resource_name, body):
    """
    This happens when a user upgrades a plan for a previously-purchased Resource.
    """
    resource = Resource().get(
        subscription_id, cloud_service_name, resource_type, resource_name)
    resource.plan = body['Resource']['Plan']
    return resource.save()
