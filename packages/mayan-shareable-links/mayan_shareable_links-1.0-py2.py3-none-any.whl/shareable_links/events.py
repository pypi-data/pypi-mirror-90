from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_('Shareable link'), name='shareable_links'
)

event_shareable_link_created = namespace.add_event_type(
    label=_('Shareable link created'), name='shareable_link_created'
)
event_shareable_link_deleted = namespace.add_event_type(
    label=_('Shareable link deleted'), name='shareable_link_deleted'
)
event_shareable_link_edited = namespace.add_event_type(
    label=_('Shareable link edited'), name='shareable_link_edited'
)
