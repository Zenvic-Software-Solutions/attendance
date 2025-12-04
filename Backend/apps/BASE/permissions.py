from rest_framework import permissions


class NonAuthenticatedAPIMixin:
    """
    A mixin that allows unrestricted access to an API endpoint
    by setting the permission classes to AllowAny.
    """
    permission_classes = [permissions.AllowAny]

class AuthenticatedAPIMixin:
    """
    A mixin that allows restricted access to an API endpoint
    by setting the permission classes to IsAuthenticated.
    """
    permission_classes = [permissions.IsAuthenticated]


from rest_framework.permissions import BasePermission


# class RoleBasedPermission(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
        
#         # Get the role and the model the view is interacting with
#         role = request.user.role
#         model_name = getattr(view, 'model_name', None)  # Set 'model_name' in the view
        
#         if not model_name:
#             return False

#         # Check the permissions for the role and model
#         try:
#             permissions = RolePermission.objects.get(role=role, model_name=model_name)
#             if request.method == "POST":  # Create
#                 return permissions.can_create
#             elif request.method in ["PUT", "PATCH"]:  # Edit
#                 return permissions.can_edit
#             elif request.method == "DELETE":  # Delete
#                 return permissions.can_delete
#             elif request.method == "GET":  # View
#                 return permissions.can_view
#         except RolePermission.DoesNotExist:
#             return False

#         return False
