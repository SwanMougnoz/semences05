from actstream import action


class ActionMessageMixin(object):

    def __init__(self):
        action.connect(self.handle_action)

    def

    def handle_action(self):
        raise NotImplementedError
