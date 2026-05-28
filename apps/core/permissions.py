from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission.
    Only the owner of an object can edit or delete it.
    Others can only read.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Write permissions only to the owner
        owner = getattr(obj, 'author', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsVerifiedUser(IsAuthenticated):
    """
    Only allows verified users.
    """
    message = 'Your account must be verified to perform this action.'

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and
            request.user.is_verified
        )


class IsThreadParticipant(BasePermission):
    """
    Only participants of a thread can read or write to it.
    """
    message = 'You are not a participant in this thread.'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()