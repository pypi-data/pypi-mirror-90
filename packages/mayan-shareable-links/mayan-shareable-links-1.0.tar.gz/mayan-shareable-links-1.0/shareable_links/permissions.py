from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_('Shareable link'), name='shareable_links'
)

permission_shareable_link_create = namespace.add_permission(
    label=_('Create shareablelinks'), name='shareable_link_create'
)
permission_shareable_link_delete = namespace.add_permission(
    label=_('Delete shareable links'), name='shareable_link_delete'
)
permission_shareable_link_edit = namespace.add_permission(
    label=_('Edit shareable links'), name='shareable_link_edit'
)
permission_shareable_link_view = namespace.add_permission(
    label=_('View shareable links'), name='shareable_link_view'
)
