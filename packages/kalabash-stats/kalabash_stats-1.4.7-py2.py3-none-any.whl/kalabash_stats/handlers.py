"""Kalabash stats signal handlers."""

from django.urls import reverse
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from kalabash.core import signals as core_signals
from kalabash.parameters import tools as param_tools

from . import graphics
from . import signals


@receiver(core_signals.extra_user_menu_entries)
def menu(sender, location, user, **kwargs):
    """Return extra menu entry."""
    if location != "top_menu" or user.role == "StandardUsers":
        return []
    return [
        {"name": "stats",
         "label": _("Statistics"),
         "url": reverse('kalabash_stats:fullindex')}
    ]


@receiver(signals.get_graph_sets)
def get_default_graphic_sets(sender, **kwargs):
    """Return graphic set."""
    mail_traffic_gset = graphics.MailTraffic(
        param_tools.get_global_parameter("greylist", raise_exception=False))
    result = {
        mail_traffic_gset.html_id: mail_traffic_gset
    }
    if kwargs.get("user").is_superuser:
        account_gset = graphics.AccountGraphicSet()
        result.update({account_gset.html_id: account_gset})
    return result
