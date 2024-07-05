# -*- coding: utf-8 -*-


class SerializerMixin(object):
    def get_permissions(self):
        try:
            self.permission_classes = self.permission_classes_by_action[self.action]
        except (KeyError, AttributeError):
            pass
        return super().get_permissions()

    def get_serializer_class(self):
        try:
            return self.serializer_class_by_action[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
