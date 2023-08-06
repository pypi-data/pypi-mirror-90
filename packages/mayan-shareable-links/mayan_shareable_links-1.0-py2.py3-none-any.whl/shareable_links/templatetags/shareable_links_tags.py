from django.apps import apps
from django.shortcuts import get_object_or_404
from django.template import Library

register = Library()


@register.simple_tag
def shareable_links_documents_get_api_image_url(
    shareable_link, document_page, **kwargs
):
    #ShareableLink = apps.get_model(
    #    app_label='shareable_links', model_name='ShareableLink'
    #)
    #get_object_or_404(klass=hareableLink, pk=


    return shareable_link.get_api_image_url(document_page=document_page, **kwargs)
