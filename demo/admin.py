from django.contrib import admin
from django.contrib import messages

from . import models

@admin.register(models.TestPerson)
class TestPersonAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        messages.debug(request, "This is a debug message")
        messages.info(request, "This is an info message")
        messages.success(request, "This is a success message")
        messages.warning(request, "This is a warning message")
        messages.error(request, "This is an error message")
        return super().changelist_view(request, extra_context)

    list_display = ("name", "age")
    search_fields = ("name", "age")
