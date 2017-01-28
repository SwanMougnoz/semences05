from actstream.managers import ActionManager, stream
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class S5ActionManager(ActionManager):

    @stream
    def others(self, obj):

        user_stream = self.user(obj)
        user_content_type = ContentType.objects.get_for_model(obj)

        return user_stream.filter(~Q(
                actor_content_type=user_content_type,
                actor_object_id=obj.id,
            ))

