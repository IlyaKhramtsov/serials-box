from django.shortcuts import Http404


class AdminAuthorPermissionMixin:
    def has_permission(self):
        return (
            self.request.user.is_superuser
            or self.request.user == self.get_object().author
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise Http404
        return super().dispatch(request, *args, **kwargs)
