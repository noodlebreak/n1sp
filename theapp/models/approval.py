from django.db import models
from django.contrib.auth.models import Group

from rulez import registry

from .user import User
from theapp.predefined import ADMIN_TYPE_TWO, ADMIN_TYPE_ONE


class Approval(models.Model):
    """
    Approval of a user by an admin.
    """

    APPROVAL_CHOICES = (
        ('A', 'Approved'),
        ('P', 'Pending'),
        ('R', 'Rejected')
    )
    for_user = models.ForeignKey(User, related_name='approvals')
    by_admin = models.ForeignKey(User)
    admin_type = models.ForeignKey(Group)
    approval = models.CharField(max_length=1, choices=APPROVAL_CHOICES,
                                default='P')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Should read like:

        <username> (admin-level-x) has approved <for_user>
        """
        done = " has approved "
        pending = "'s approval for "
        middle = [pending, done][self.approval == 'A']
        representation = self.admin_type.name + self.by_admin.username \
            + middle + self.for_user.username
        return representation

    def can_be_approved_by(self, user_obj):
        '''
        Returns a bool, depending on whether
        the acting admin/user CAN approve the
        user, given the requirements of business logic.
        '''

        # ADMIN TYPE 2 can approve ALL
        if user_obj.groups.filter(name=ADMIN_TYPE_TWO).exists():
            return True

        # ADMIN TYPE 1 users from his city only
        if user_obj.groups.filter(name=ADMIN_TYPE_ONE).exists():
            if user_obj.location == self.for_user.location:
                return True

        # Not an admin
        # OR, admin is type 1, and user is not in his location
        return False

    def mark_approved(self):
        self.approval = 'A'
        self.save()

registry.register('can_be_approved_by', Approval)
