# connection to client, mock implementation will reside in this file.
# all the data will be sent through this file using the publish method define
# below.

# The implementation of publish method will need to be changed here from
# time to time.

from omnibus import api
omnibus = ''


def publish(channel, payload_type, payload=None, sender=None):
    """
    calling this publish method sends a push
    notification to all the registered clients

    :param channel: name of the channel
    :param payload_type: the `type` of the message/event,
    clients use this name to register event handlers
    :param payload: payload of the event, needs to be
    a dict which is JSON dumpable.
    """
    return api.publish(channel, payload_type, payload, sender)
