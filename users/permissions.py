from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    """
    Permission для модераторов:
    - is_staff=True
    - Может читать, изменять и удалять продукты и категории
    - POST запрещён
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if not request.user.is_staff:
            return False
        if request.method == 'POST':
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return False