from django.db.models.signals import post_save
from django.dispatch import receiver

from theapp.models import Notification
from theapp.publish import publish
from theapp.models import EmailVerification
from theapp.models import User, Approval
from theapp.predefined import ADMIN_TYPE_ONE
from theapp.predefined import ADMIN_TYPE_TWO


@receiver(post_save, sender=EmailVerification)
def set_token(created, instance, **kwargs):

    if created:
        instance.token = instance.create_token()
        instance.save()


@receiver(post_save, sender=Approval)
def approval_post_save(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if not created:
        if instance.approval == 'A':
            # Approved

            # Notify the user approved
            Notification.objects.create(
                receiver=instance.for_user,
                approval=instance)

            # Notify admin type 2
            # if approved by 1
            if instance.by_admin.groups.filter(
                    name=ADMIN_TYPE_ONE).exists():
                admin_t2 = User.objects.filter(
                    groups__name=ADMIN_TYPE_TWO).first()
                Notification.objects.create(
                    receiver=admin_t2,
                    approval=instance)

            # Notify admin type 1
            # if approved by 2
            if instance.by_admin.groups.filter(
                    name=ADMIN_TYPE_TWO).exists():
                admin_t1 = User.objects.filter(
                    groups__name=ADMIN_TYPE_ONE).first()
                Notification.objects.create(
                    receiver=admin_t1,
                    approval=instance)

            print("Created notifications for approval #%d" % instance.pk)


@receiver(post_save, sender=Notification)
def notification_post_save(**kwargs):
    print("Creating push notif ...")
    if kwargs.get('created'):
        _n = kwargs.get('instance', None)
        n_data = {
            'message': str(_n.approval),
            'timestamp': str(_n.created_on),
        }
        publish(channel=str(_n.receiver.pk),

                # It would have been _n.action's model_name in the generic one
                payload_type='approval',

                payload=n_data,
                sender='n1sp')
        print("Sent push notif %d" % _n.pk)
