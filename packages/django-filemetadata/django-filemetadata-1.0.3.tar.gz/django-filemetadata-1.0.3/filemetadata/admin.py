from django.contrib import admin

from .models import FileMetadata

@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ('filename', 'path', 'size_str')
    list_filter = ('path', 'suffix')

