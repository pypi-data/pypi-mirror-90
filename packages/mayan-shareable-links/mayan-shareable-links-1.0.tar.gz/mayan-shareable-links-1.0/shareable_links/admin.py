from django.contrib import admin

from .models import ShareableLink


@admin.register(ShareableLink)
class ShareableLinkAdmin(admin.ModelAdmin):
    list_display = ('document', 'uuid', 'description')
