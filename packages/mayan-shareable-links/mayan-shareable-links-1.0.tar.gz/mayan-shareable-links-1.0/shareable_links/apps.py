import logging

from django.apps import apps
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.acls.links import link_acl_list
from mayan.apps.acls.permissions import permission_acl_edit, permission_acl_view
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_object, menu_secondary, menu_setup
)
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from mayan.apps.events.permissions import permission_events_view
from mayan.apps.navigation.classes import SourceColumn

from .events import event_shareable_link_edited
from .links import (
    link_document_shareable_link_list, link_shareable_link_delete,
    link_shareable_link_edit, link_shareable_link_list,
    link_shareable_link_setup
)
from .permissions import (
    permission_shareable_link_delete, permission_shareable_link_edit,
    permission_shareable_link_view
)

logger = logging.getLogger(name=__name__)


class ShareableLinkApp(MayanAppConfig):
    app_namespace = 'shareable_links'
    app_url = 'shareable_links'
    has_rest_api = True
    has_tests = True
    name = 'shareable_links'
    verbose_name = _('Shareable links')

    def ready(self):
        super().ready()

        ShareableLink = self.get_model(model_name='ShareableLink')

        Document = apps.get_model(app_label='documents', model_name='Document')

        EventModelRegistry.register(model=ShareableLink)

        ModelEventType.register(
            model=ShareableLink, event_types=(
                event_shareable_link_edited,
            )
        )

        SourceColumn(
            attribute='uuid', is_identifier=True, is_sortable=True,
            source=ShareableLink
        )
        #SourceColumn(
        #    attribute='description', include_label=True,
        #    source=ShareableLink
        #)
        SourceColumn(
            func=lambda context: reverse(
                viewname='shareable_links:shareable_link_use', kwargs={
                    'uuid': context['object'].uuid
                }
            ), label=_('URL'), source=ShareableLink
        )

        ModelPermission.register(
            model=ShareableLink, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_shareable_link_delete,
                permission_shareable_link_edit, permission_shareable_link_view,
            )
        )

        menu_list_facet.bind_links(
            links=(
                link_document_shareable_link_list,
            ), sources=(Document,)
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
            ), sources=(ShareableLink,)
        )

        menu_object.bind_links(
            links=(
                link_shareable_link_delete,
                #link_shareable_link_edit,
            ), sources=(ShareableLink,)
        )

        menu_secondary.bind_links(
            links=(
                #link_shareable_link_create,
                link_shareable_link_list,
            ), sources=(
                ShareableLink,
                'shareable_links:stored_shareable_link_create',
                'shareable_links:stored_shareable_link_list'
            )
        )

        #menu_setup.bind_links(
        #    links=(link_shareable_link_setup,)
        #)
