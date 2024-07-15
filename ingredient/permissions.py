from account.permissions import IsAdmin


class IsPostAndIsAdmin(IsAdmin):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return super().has_permission(request, view)
        return True
