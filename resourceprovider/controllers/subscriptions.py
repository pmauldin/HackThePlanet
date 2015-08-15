"""
TODO: what are the subscription controllers?
"""
from resourceprovider.models import Subscription, Event
from datetime import datetime


def _log_event(body):
    event_opts = {
        '_id': body['EntityEvent']['OperationId']
    }
    event_opts.update(body)
    return Event(**event_opts).save()


def registered(subscription_id, body):
    """
    This tells the RP that the user intends to create a resource under this subscription.
    """
    sub_opts = {
        '_id': subscription_id,
        'created_date': body['EntityEvent']['EntityId']['Created']
    }
    sub_opts.update(body)
    subscription = Subscription(**sub_opts).save()
    return subscription, _log_event(body)


def disabled(subscription_id, body):
    """
    The user's Windows Azure subscription has been disabled, due to fraud or non-payment.
    Your RP should make the resource inaccessible without deleting its data.
    """
    subscription = Subscription().get(subscription_id)
    subscription.state = 'disabled'
    subscription.save()
    return subscription, _log_event(body)


def enabled(subscription_id, body):
    """
    The user's Windows Azure subscription has been enabled, because it is current on payments.
    Your RP should restore access to data.
    """
    subscription = Subscription().get(subscription_id)
    subscription.state = 'enabled'
    subscription.save()
    return subscription, _log_event(body)


def deleted(subscription_id, body):
    """
    The user's Windows Azure subscription has been deleted.
    Disable access permanently, but ensure the data is retained for at least 90 days.
    """
    subscription = Subscription().get(subscription_id).delete()
    return subscription, _log_event(body)
