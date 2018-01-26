from django.contrib import admin

from . import models


class ContactAdmin(admin.ModelAdmin):
    list_filter = ('state',)
    search_fields = ('name', 'email', 'message',)
    readonly_fields = (
        'name', 'email', 'message', 'created_at', 'modified_at', 'uuid',
    )
    fields = ('state',) + readonly_fields[:3] + ('notes',) + readonly_fields[3:]


admin.site.register(models.Contact, ContactAdmin)
