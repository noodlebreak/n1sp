from django.contrib.contenttypes.models import ContentType
from django.utils.lru_cache import lru_cache

from theapp.models import Notification


@lru_cache(maxsize=512)
def get_content_type(model):
    return ContentType.objects.get_for_model(model)


def create_notification(actor_content_type, actor_object_id,
                        verb, user, action_content_type=None,
                        action_object_id=None, target_content_type=None,
                        target_object_id=None, is_read=False):
    n = Notification(actor_content_type=actor_content_type,
                     actor_object_id=actor_object_id,
                     verb=verb, user=user,
                     action_content_type=action_content_type,
                     action_object_id=action_object_id,
                     target_content_type=target_content_type,
                     target_object_id=target_object_id, is_read=is_read)
    n.save()
    return n
