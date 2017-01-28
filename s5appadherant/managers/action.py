from actstream.managers import ActionManager, stream
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class S5ActionManager(ActionManager):

    def get_by_terms(self, verb, action_object, target):
        action_object_content_type = ContentType.objects.get_for_model(action_object)
        target_content_type = ContentType.objects.get_for_model(target)

        return self.get(action_object_object_id=action_object.id,
                        action_object_content_type_id=action_object_content_type.id,
                        target_content_type_id=target_content_type.id,
                        target_object_id=target.id,
                        verb=verb)

    @stream
    def self_excluded_unprocessed(self, obj):
        user_stream = self.user(obj)
        user_content_type = ContentType.objects.get_for_model(obj)

        return user_stream.filter(~Q(
            actor_content_type=user_content_type,
            actor_object_id=obj.id
        ), processed__isnull=True)
