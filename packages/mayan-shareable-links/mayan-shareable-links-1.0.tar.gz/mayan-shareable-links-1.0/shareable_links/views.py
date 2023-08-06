import logging

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from stronghold.views import StrongholdPublicMixin

from mayan.apps.common.generics import (
    FormView, SingleObjectDeleteView, SingleObjectCreateView,
    SingleObjectDownloadView, SingleObjectListView, SimpleView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.models import Document
from mayan.apps.documents.settings import (
    setting_print_height, setting_print_width
)

from .icons import icon_shareable_links
#from .links import link_stored_shareable_link_backend_selection
from .models import ShareableLink
from .permissions import (
    permission_shareable_link_create, permission_shareable_link_delete,
    permission_shareable_link_edit, permission_shareable_link_view
)

logger = logging.getLogger(name=__name__)


class ShareableLinkDocumentDownloadView(
    StrongholdPublicMixin, SingleObjectDownloadView
):
    model = ShareableLink
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_download_file_object(self):
        return self.object.document.open()

    def get_download_label(self):
        return force_text(self.object.document)


# StrongholdPublicMixin needs to be first
class ShareableLinkDocumentPreviewView(
    StrongholdPublicMixin, ExternalObjectMixin, SimpleView
):
    external_object_class = ShareableLink
    external_object_pk_url_kwargs = {'uuid': 'uuid'}
    template_name = 'shareable_links/document_preview.html'

    def get_extra_context(self):
        context = {
            'appearance_type': 'plain',
            'shareable_link': self.external_object,
            'pages': self.external_object.document.pages.all(),
            'width': setting_print_width.value,
            'height': setting_print_height.value,
        }

        return context


class ShareableLinkCreateView(SingleObjectCreateView):
    post_action_redirect = reverse_lazy(
        viewname='shareable_links:stored_shareable_link_list'
    )
    view_permission = permission_shareable_link_create

    def get_backend(self):
        try:
            return CredentialBackend.get(name=self.kwargs['class_path'])
        except KeyError:
            raise Http404(
                '{} class not found'.format(self.kwargs['class_path'])
            )

    def get_extra_context(self):
        return {
            'title': _(
                'Create a new shareable link.'
            ) % self.get_backend().label,
        }

    def get_form_schema(self):
        backend = self.get_backend()
        result = {
            'fields': backend.fields,
            'widgets': getattr(backend, 'widgets', {})
        }
        if hasattr(backend, 'field_order'):
            result['field_order'] = backend.field_order

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['class_path']
        }


class ShareableLinkDeleteView(SingleObjectDeleteView):
    model = ShareableLink
    object_permission = permission_shareable_link_delete
    pk_url_kwarg = 'shareable_link_id'
    post_action_redirect = reverse_lazy(
        viewname='shareable_links:stored_shareable_link_list'
    )

    def get_extra_context(self):
        return {
            'title': _('Delete shareable link: %s') % self.object,
        }


class DocumentShareableLinkListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_shareable_link_view
    external_object_pk_url_kwarg = 'document_id'
    object_permission = permission_shareable_link_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            #'hide_link': True,
            #'no_results_main_link': link_document_tag_multiple_attach.resolve(
            #    context=RequestContext(
            #        self.request, {'object': self.external_object}
            #    )
            #),
            'no_results_icon': icon_shareable_links,
            'no_results_text': _(
                'Shareable links give controlled access to document actions '
                'to external users.'
            ),
            'no_results_title': _('Document has no shareable links'),
            'object': self.external_object,
            'title': _(
                'Shareable links for document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.shareable_links.all()
