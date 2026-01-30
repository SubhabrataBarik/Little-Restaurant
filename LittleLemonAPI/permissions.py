from rest_framework.permissions import BasePermission, IsAuthenticated

class IsManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and request.user.groups.filter(name='Delivery crew').exists())
