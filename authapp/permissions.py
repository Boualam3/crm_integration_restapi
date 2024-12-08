from rest_framework.permissions import IsAuthenticated, BasePermission


class IsOwner(BasePermission):
    """
     permission to ensure that the user can only access or modify their own profile.
    """

    def has_object_permission(self, request, view, obj):

        return obj == request.user
