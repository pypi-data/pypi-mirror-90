import uuid

from furl import furl

from django.db import models
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.transformations import BaseTransformation
from mayan.apps.documents.models import Document, DocumentPage
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event

from .events import event_shareable_link_created, event_shareable_link_edited


class ShareableLink(models.Model):
    document = models.ForeignKey(
        help_text=_('The document to which to link.'),
        on_delete=models.CASCADE, related_name='shareable_links',
        to=Document, verbose_name=_('Document')
    )
    description = models.TextField(
        blank=True, help_text=_('Text describing of this link.'),
        verbose_name=_('Description')
    )
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, help_text=_(
            'Universally Unique ID. A unique identifier generated for each '
            'link.'
        ), verbose_name=_('UUID')
    )

    class Meta:
        #unique_together = ('uuid', 'document')
        verbose_name = _('Shareable link')
        verbose_name_plural = _('Shareable links')

    def get_api_image_url(self, document_page, *args, **kwargs):
        """
        Create an unique URL combining:
        - the page's image URL
        - the interactive argument
        - a hash from the server side and interactive transformations
        The purpose of this unique URL is to allow client side caching
        if document page images.
        """
        document_page = DocumentPage.objects.filter(
            document_version__document__id=self.document_id
        ).get(pk=document_page.pk)

        transformations_hash = BaseTransformation.combine(
            document_page.get_combined_transformation_list(*args, **kwargs)
        )

        kwargs.pop('transformations', None)

        final_url = furl()
        final_url.args = kwargs
        final_url.path = reverse(
            viewname='rest_api:shareablelink-documentpage-image', kwargs={
                'shareable_link_id': self.pk,
                'document_version_id': document_page.document_version.pk,
                'document_page_id': document_page.pk
            }
        )
        final_url.args['_hash'] = transformations_hash

        return final_url.tostr()

    def __str__(self):
        return str(self.uuid)
    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_shareable_link_created,
            'target': 'self',
        },
        edited={
            'event': event_shareable_link_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
