from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        messages.success(request, "This is a success message")
        messages.warning(request, "This is a warning message")

        messages.info(request, "This is an info message", extra_tags="info")

        messages.error(request, "This is an error message")
        return super().index(request, extra_context)


custom_admin_site = CustomAdminSite(name="custom_admin")

# Register User and Group models with the custom admin site
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
