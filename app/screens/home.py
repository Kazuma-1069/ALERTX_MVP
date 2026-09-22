"""AlertX Home Screen.

Presents primary SOS emergency trigger button, real-time protection telemetry,
and rapid navigation to emergency contacts and safety status.
Follows Google Stitch Guardian Modern design system.
"""

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from services.emergency import get_primary_contact


class HomeScreen(Screen):
    contact_name = StringProperty("Sarah Jenkins (Spouse)")
    contact_phone = StringProperty("+1 (555) 234-5678")
    contact_badge = StringProperty("Ready")
    location_title = StringProperty("Precise Location Active")
    location_subtitle = StringProperty("GPS Acquired • Live")
    sos_status_text = StringProperty("Hold 2s to Prevent False Alarms")
    online_badge_text = StringProperty("ONLINE")
    defense_summary = StringProperty(
        "Your safety system is armed. In an emergency, pressing SOS will immediately alert Sarah Jenkins with your real-time satellite coordinates."
    )
    defense_summary_markup = StringProperty("")
    contact_markup = StringProperty("")
    location_markup = StringProperty("")
    banner_markup = StringProperty(
        "[b][size=16sp][color=F8FAFC]ALERTX[/color][/size][/b]   [b][size=10sp][color=38BDF8]PRO[/color][/size][/b]\n"
        "[size=11sp][color=94A3B8]Personal Safety Guard[/color][/size]"
    )

    _sos_hold_event = None
    _sos_hold_start = 0.0

    def on_enter(self):
        self.refresh()

    def refresh(self):
        """Update contact and telemetry widgets with latest state."""
        contact = get_primary_contact()
        if contact:
            rel = contact.get("relationship", "Contact")
            self.contact_name = f"{contact['name']} ({rel})" if rel else contact["name"]
            self.contact_phone = contact.get("phone", "")
            self.contact_badge = "Ready" if contact.get("is_enabled", True) else "Disabled"
            self.defense_summary = (
                f"Your safety system is armed. In an emergency, pressing SOS will immediately alert "
                f"{contact['name']} with your real-time satellite coordinates."
            )
        else:
            self.contact_name = "No contact saved"
            self.contact_phone = "Tap to configure primary guardian"
            self.contact_badge = "Setup"
            self.defense_summary = (
                "No primary emergency contact configured. Add a contact in the Contacts tab to arm the system."
            )

        self.defense_summary_markup = (
            f"[b][color=F8FAFC]System Defense Ready[/color][/b]\n"
            f"[size=11sp][color=94A3B8]{self.defense_summary}[/color][/size]"
        )

        self.contact_markup = (
            f"[b][size=10sp][color=94A3B8]EMERGENCY CONTACT[/color][/size][/b]\n"
            f"[b][size=14sp][color=F8FAFC]{self.contact_name}[/color][/size][/b]\n"
            f"[size=11sp][color=94A3B8]{self.contact_phone}[/color][/size]"
        )

        # Telemetry updates
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, "location"):
            loc = app.location.get_current()
            if loc.get("ok"):
                self.location_title = "Precise Location Active"
                self.location_subtitle = f"GPS Acquired • {loc.get('accuracy_str', 'Live')}"
            else:
                self.location_title = "Location Services"
                self.location_subtitle = "Acquiring GPS fix..."

        self.location_markup = (
            f"[b][size=10sp][color=94A3B8]LOCATION SERVICES[/color][/size][/b]\n"
            f"[b][size=14sp][color=F8FAFC]{self.location_title}[/color][/size][/b]\n"
            f"[size=11sp][color=94A3B8]{self.location_subtitle}[/color][/size]"
        )

        if hasattr(app, "api") and app.api:
            self.online_badge_text = "ONLINE" if app.api.is_online else "STANDALONE"

    def on_sos_press(self):
        """Called when user touches down on SOS button."""
        import time
        self._sos_hold_start = time.time()
        self.sos_status_text = "HOLD FOR 2 SECONDS..."
        if self._sos_hold_event:
            self._sos_hold_event.cancel()
        self._sos_hold_event = Clock.schedule_once(self._on_sos_hold_completed, 2.0)

    def on_sos_release(self):
        """Called when user lifts finger from SOS button."""
        if self._sos_hold_event:
            self._sos_hold_event.cancel()
            self._sos_hold_event = None
            self.sos_status_text = "Hold 2s to Prevent False Alarms"

    def _on_sos_hold_completed(self, dt):
        """Fired after 2 full seconds of holding down SOS."""
        self._sos_hold_event = None
        self.sos_status_text = "EMERGENCY DISPATCHING..."
        self.trigger_sos()

    def trigger_sos(self):
        """Activate emergency dispatch."""
        self.sos_status_text = "Hold 2s to Prevent False Alarms"
        from kivy.app import App
        App.get_running_app().start_emergency()

