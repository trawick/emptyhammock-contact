from django.contrib import admin

from . import models


class ContactAdmin(admin.ModelAdmin):
    list_filter = ('state',)
    search_fields = ('name', 'email', 'message',)
    readonly_fields = (
        'state', 'name', 'email', 'message', 'created_at', 'modified_at', 'uuid',
    )
    fields = readonly_fields[:4] + ('notes',) + readonly_fields[4:]


admin.site.register(models.Contact, ContactAdmin)
