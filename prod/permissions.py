from rest_framework.permissions import BasePermission, SAFE_METHODS

class PotomPridumayuNazvanie(BasePermission):
    """Читать конкретный пост может каждый,
    исправлять/удалять свой пост может автор или супер юзер или админ
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and 
            obj.author == request.user or 
            (request.user.is_superuser or request.user.is_staff)
        )