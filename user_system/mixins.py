from user_system.models import CustomUser
from django.core.exceptions import PermissionDenied


class RequestUserIsUserMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()

        if CustomUser.objects.get(pk=request.user.pk) == instance:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class UserIsOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.objects.filter(author=request.user):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied