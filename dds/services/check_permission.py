def check_permission(request):
    if request.user and (request.user.is_superuser or request.user.role == 'admin'):
        return True
    return False
