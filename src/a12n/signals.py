from rest_framework.exceptions import PermissionDenied


def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")
