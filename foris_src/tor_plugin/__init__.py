import os
import syslog

from foris.config import ConfigPageMixin, add_config_page
from foris.config_handlers import BaseConfigHandler
from foris.core import gettext_dummy as gettext, ugettext as _
from foris.plugins import ForisPlugin
from foris import validators
from foris.fapi import ForisForm
from foris.form import MultiCheckbox,Checkbox, Textbox
from foris.form import Number
from foris.nuci.filters import create_config_filter
from foris.nuci.modules.uci_raw import Uci, Config, Section, Option
from foris.nuci.modules.uci_raw import Uci, Config, Section, Option

class TorPluginConfigHandler(BaseConfigHandler):
    @staticmethod
    def preproc_slices(option):
        return int(option.value)

    def get_form(self):
        form = ForisForm(
            "tor_plugin_check", self.data, filter=None #create_config_filter("tor_plugin")
        )
	section = form.add_section(name="parameters", title=_("Tor configuration"))
	section.add_field(
	Checkbox, name="default_tor_route", label=_("All traffic through tor"),
		hint=_(
		"After enabling this option all traffic from your client "
		"will be routed through the tor network."
		),
	)

        def update_uci_callback(data):
	    enable_route=data["default_tor_route"]
	    print form.nuci_config().find_child("uci.tor.omnia_specific.enable_routing").value
	    if enable_route:
	    	print "Selected"
	    else:
	    	print "Unselected"
            syslog.syslog("update_uci_callback")
            return "none",None

        def update_program_callback(data):
            syslog.syslog("foris tor plugin update_program_callback")
            return "none", None

        form.add_callback(update_uci_callback)
        #form.add_callback(update_program_callback)
        return form

class TorPluginPage(ConfigPageMixin, TorPluginConfigHandler):
    menu_order = 1
    template = "tor_plugin/tor_plugin.tpl"
    userfriendly_title = gettext("TOR plugin")


class TorPluginPlugin(ForisPlugin):
    PLUGIN_NAME = "tor_plugin"
    DIRNAME = os.path.dirname(os.path.abspath(__file__))

    PLUGIN_STYLES = [
    ]
    PLUGIN_STATIC_SCRIPTS = [
    ]
    PLUGIN_DYNAMIC_SCRIPTS = [
    ]

    def __init__(self, app):
        super(TorPluginPlugin, self).__init__(app)
        add_config_page("tor_plugin", TorPluginPage, top_level=True)
