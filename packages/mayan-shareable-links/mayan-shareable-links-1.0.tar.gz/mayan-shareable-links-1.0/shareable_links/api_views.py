from django.shortcuts import get_object_or_404

from mayan.apps.documents.api_views import APIDocumentPageImageView
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.rest_api import generics

from .models import ShareableLink
from .permissions import (
    permission_shareable_link_create, permission_shareable_link_delete,
    permission_shareable_link_edit, permission_shareable_link_view
)
from .serializers import DocumentShareableLinkSerializer


class APIDocumentShareableLinkListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the shareable link of the selected document.
    post: Create a new shareable link for the selected document.
    """
    mayan_object_permissions = {
        'GET': (permission_shareable_link_view,),
        'POST': (permission_shareable_link_view,),
    }
    serializer_class = DocumentShareableLinkSerializer

    def perform_create(self, serializer):
        serializer.validated_data['document'] = self.get_document()
        serializer.save()

    def get_document(self):
        return get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

    def get_queryset(self):
        return self.get_document().shareable_links.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)


class APIDocumentShareableLinkDetailView(generics.RetrieveDestroyAPIView):
    """
    delete: Delete the selected shareable link.
    get: Return the details of the selected shareable link.
    """
    lookup_url_kwarg = 'shareable_link_id'
    mayan_object_permissions = {
        'DELETE': (permission_shareable_link_delete,),
        'GET': (permission_shareable_link_view,),
    }
    serializer_class = DocumentShareableLinkSerializer

    def get_document(self):
        return get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

    def get_queryset(self):
        return self.get_document().shareable_links.all()

    def get_serializer(self, *args, **kwargs):
        if not self.request:
            return None

        return super().get_serializer(*args, **kwargs)


class APIShareableLinkDocumentPageImageView(APIDocumentPageImageView):
    lookup_url_kwarg = 'document_page_id'

    def get_document_version(self):
        return get_object_or_404(
            self.get_document().versions.all(), pk=self.kwargs[
                'document_version_id'
            ]
        )

    def get_document(self):
        return self.get_shareable_link().document

    def get_shareable_link(self):
        return get_object_or_404(
            klass=ShareableLink, pk=self.kwargs['shareable_link_id']
        )
