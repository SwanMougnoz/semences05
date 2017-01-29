from actstream.managers import ActionManager, stream
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class S5ActionManager(ActionManager):

    def get_by_terms(self, verb=None, action_object=None, target=None):
        filters = {}

        if verb:
            filters.update({
                'verb': verb
            })

        if action_object:
            action_object_content_type = ContentType.objects.get_for_model(action_object)
            filters.update({
                'action_object_object_id': action_object.id,
                'action_object_content_type_id': action_object_content_type.id
            })

        if target:
            target_content_type = ContentType.objects.get_for_model(target)
            filters.update({
                'target_content_type_id': target_content_type.id,
                'target_object_id': target.id
            })

        return self.get(**filters)

    @stream
    def self_excluded_unprocessed(self, obj):
        user_stream = self.user(obj)
        user_content_type = ContentType.objects.get_for_model(obj)

        return user_stream.filter(~Q(
            actor_content_type=user_content_type,
            actor_object_id=obj.id
        )).exclude(adherant_has_proceed=obj.adherant)
