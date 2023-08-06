from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_cascade_condition

from .icons import (
    icon_shareable_link_delete, icon_shareable_link_edit,
    icon_shareable_link_list, icon_shareable_link_setup
)
from .permissions import (
    permission_shareable_link_create, permission_shareable_link_delete,
    permission_shareable_link_edit, permission_shareable_link_view
)

#link_shareable_link_backend_selection = Link(
#    icon_class=icon_shareable_link_backend_selection,
#    permissions=(permission_shareable_link_create,),
#    text=_('Create shareable link'),
#    view='shareable_links:shareable_link_backend_selection',
#)
link_shareable_link_delete = Link(
    args='resolved_object.pk',
    icon_class=icon_shareable_link_delete,
    permissions=(permission_shareable_link_delete,),
    tags='dangerous', text=_('Delete'),
    view='shareable_links:shareable_link_delete',
)
link_shareable_link_edit = Link(
    args='object.pk',
    icon_class=icon_shareable_link_edit,
    permissions=(permission_shareable_link_edit,),
    text=_('Edit'), view='shareable_links:shareable_link_edit',
)
link_shareable_link_list = Link(
    icon_class=icon_shareable_link_list,
    permissions=(permission_shareable_link_view,),
    text=_('Shareable link list'), view='shareable_links:shareable_link_list',
)
link_document_shareable_link_list = Link(
    args='resolved_object.pk', icon_class=icon_shareable_link_list,
    permissions=(permission_shareable_link_view,),
    text=_('Shareable links'),
    view='shareable_links:document_shareable_link_list',
)
link_shareable_link_setup = Link(
    condition=get_cascade_condition(
        app_label='shareable_links', model_name='SharebleLink',
        object_permission=permission_shareable_link_view,
        view_permission=permission_shareable_link_create,
    ), icon_class=icon_shareable_link_setup,
    text=_('Shareable links'),
    view='shareable_links:shareable_link_list'
)
