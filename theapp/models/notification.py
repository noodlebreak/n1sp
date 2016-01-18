from django.db import models
from .user import User
from .approval import Approval


class Notification(models.Model):
    """
    A very dumbed down, this app
    specific notification model
    describing an actor acting out a verb.

    Not using GFKs to use it for any type of
    models for actors, actions, and targets.

    actor  -  Person who took some action
    verb   -  Describing the action taken
    action -  Action model that stores a record of action
    target -  Person affected or involved in action
    user   -  Person who gets notified

    Basically, something like this:
    <actor> <verb>AND/OR<action> <target>

    Examples:
    <actor> <verb> <target>
    Jack approved John

    <actor> <verb> <action>
    Jack reached level-3

    <actor> <verb> <action> <target>
    Rimi started following Jackie
    """

    # The person who gets notified
    receiver = models.ForeignKey(User, related_name='notification_receiver')

    # The approval for which the notification is created
    approval = models.ForeignKey(Approval, related_name='actor')

    is_read = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
