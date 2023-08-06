from django.db import models
from django.utils.translation import ugettext_lazy as _


class FileMetadata(models.Model):
    inode = models.IntegerField(db_index=True, verbose_name=_('inode'))
    filename = models.TextField(blank=True, null=True, verbose_name=_('Filename'))
    suffix = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('Suffix'))
    path = models.TextField(blank=True, null=True, verbose_name=_('Path'))
    size = models.IntegerField(blank=True, null=True, verbose_name=_('Size (bits)'))
    size_str = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('Size'))
    created = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=_('Created'))
    modified = models.DateTimeField(blank=True, auto_now_add=True, verbose_name=_('Modified'))
    title = models.CharField(blank=True, null=True, max_length=256, verbose_name=_('Title'))
    description = models.CharField(blank=True, null=True, max_length=256, verbose_name=_('Description'))
    text_content = models.TextField(blank=True, null=True, verbose_name=_('Text content'))

    class Meta:
        verbose_name = _('static file')
        verbose_name_plural = _('static files')

    def __repr__(self):
        # return '<StaticPage: %s -- %s>' % (self.url, truncatewords_html(self.content, 10))
        return self.name
