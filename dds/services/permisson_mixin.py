from django.core.exceptions import PermissionDenied


class PermissionMixin(object):

    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied()
        else:
            return obj
