from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.documents.serializers import DocumentSerializer

from .models import ShareableLink


def get_document_shareable_link_list_url(self, instance):
    return reverse(
        viewname='rest_api:document-shareablelink-list', kwargs={
            'document_id': instance.pk
        }, request=self.context['request'], format=self.context['format']
    )


DocumentSerializer._declared_fields['shareable_link_list_url'] = serializers.SerializerMethodField()#source='object_get_object_shareable_link_list_url')
DocumentSerializer.get_shareable_link_list_url = get_document_shareable_link_list_url
DocumentSerializer.Meta.fields += ('shareable_link_list_url',)


class DocumentShareableLinkSerializer(serializers.ModelSerializer):
    action_urls = serializers.SerializerMethodField()
    document = DocumentSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'action_urls', 'description', 'document', 'id',
            'url', 'uuid'
        )
        model = ShareableLink

    def get_action_urls(self, instance):
        return {
            'document_download_url': reverse(
                viewname='shareable_links:shareable_link_document_download',
                kwargs={
                    'uuid': instance.uuid
                }, request=self.context['request'],
            ),
            'document_preview_url': reverse(
                viewname='shareable_links:shareable_link_document_preview',
                kwargs={
                    'uuid': instance.uuid
                }, request=self.context['request'],
            )
        }

    def get_url(self, instance):
        return reverse(
            'rest_api:document-shareablelink-detail', kwargs={
                'document_id': instance.document.pk,
                'shareable_link_id': instance.pk
            }, request=self.context['request'], format=self.context['format']
        )
