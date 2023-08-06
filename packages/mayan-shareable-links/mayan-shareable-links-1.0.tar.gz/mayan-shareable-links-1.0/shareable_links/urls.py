from django.conf.urls import url
from django.urls import path

from .api_views import (
    APIDocumentShareableLinkDetailView, APIDocumentShareableLinkListView,
    APIShareableLinkDocumentPageImageView
)
from .views import (
    DocumentShareableLinkListView, ShareableLinkDocumentDownloadView,
    ShareableLinkDocumentPreviewView, ShareableLinkDeleteView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/shareable_links/$',
        name='document_shareable_link_list',
        view=DocumentShareableLinkListView.as_view()
    ),
    #url(
    #    regex=r'^documents/(?P<document_id>\d+)/shareable_links/create/$',
    #    name='document_shareable_link_create',
    #    view=DocumentShareableLinkCreateView.as_view()
    #),
    url(
        regex=r'^shareable_links/(?P<shareable_link_id>\d+)/delete/$',
        name='shareable_link_delete',
        view=ShareableLinkDeleteView.as_view()
    ),
    #url(
    #    regex=r'^shareable_links/(?P<uuid>[a-zA-Z0-9_.]+)/use/$',
    #    name='shareable_link_use',
    #    view=ShareableLinkUseView.as_view()
    #),
    path(
        route='shareable_links/<uuid>/document/preview/',
        name='shareable_link_document_preview',
        view=ShareableLinkDocumentPreviewView.as_view()
    ),
    path(
        route='shareable_links/<uuid>/document/download/',
        name='shareable_link_document_download',
        view=ShareableLinkDocumentDownloadView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/shareable_links/$',
        name='document-shareablelink-list',
        view=APIDocumentShareableLinkListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/shareable_links/(?P<shareable_link_id>[0-9]+)/$',
        name='document-shareablelink-detail',
        view=APIDocumentShareableLinkDetailView.as_view()
    ),



    #url(
    #    regex=r'^shareable_links/$', name='shareablelink-list',
    #    view=APIShareableLinkListView.as_view()
    #),
    #url(
    #    regex=r'^shareable_links/(?P<shareable_link_id>[0-9]+)/$',
    #    name='shareablelink-detail', view=APIShareableLinkDetailView.as_view()
    #),
    url(
        #regex=r'^shareable_links/(?P<shareable_link_id>[0-9]+)/documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/(?P<document_page_id>[0-9]+)/image/$',
        regex=r'^shareable_links/(?P<shareable_link_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/pages/(?P<document_page_id>[0-9]+)/image/$',
        name='shareablelink-documentpage-image',
        view=APIShareableLinkDocumentPageImageView.as_view()
    ),
]
