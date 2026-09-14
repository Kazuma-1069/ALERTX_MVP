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
    defense_summary = StringProperty(
        "Your safety system is armed. In an emergency, pressing SOS will immediately alert Sarah Jenkins with your real-time satellite coordinates."
    )
    defense_summary_markup = StringProperty("")
    contact_markup = StringProperty("")
    location_markup = StringProperty("")
    banner_markup = StringProperty(
        "[b][size=17sp][color=0B1C30]ALERTX[/color][/size][/b]   [b][size=10sp][color=0051D5]PRO[/color][/size][/b]\n"
        "[size=12sp][color=45464D]Personal Safety Guard[/color][/size]"
    )

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
            f"[b][color=0B1C30]System Defense Ready[/color][/b]\n"
            f"[size=11sp][color=45464D]{self.defense_summary}[/color][/size]"
        )

        self.contact_markup = (
            f"[b][size=10sp][color=45464D]EMERGENCY CONTACT[/color][/size][/b]\n"
            f"[b][size=15sp][color=0B1C30]{self.contact_name}[/color][/size][/b]\n"
            f"[size=12sp][color=45464D]{self.contact_phone}[/color][/size]"
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
            f"[b][size=10sp][color=45464D]LOCATION SERVICES[/color][/size][/b]\n"
            f"[b][size=15sp][color=0B1C30]{self.location_title}[/color][/size][/b]\n"
            f"[size=12sp][color=45464D]{self.location_subtitle}[/color][/size]"
        )

    def trigger_sos(self):
        """Activate emergency dispatch."""
        from kivy.app import App
        App.get_running_app().start_emergency()
