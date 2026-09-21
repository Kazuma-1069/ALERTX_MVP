"""AlertX Emergency Contacts Screen.

Implements contact configuration, relationship categorization, test alerts,
and multi-contact management following Stitch design specifications.
"""

from kivy.clock import Clock
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from services.emergency import (
    delete_contact,
    get_primary_contact,
    load_contacts,
    save_or_update_contact,
    toggle_contact_enabled,
)


class ContactsScreen(Screen):
    guardian_initials = StringProperty("SJ")
    guardian_name = StringProperty("Sarah Jenkins")
    guardian_relation = StringProperty("Spouse")
    guardian_phone = StringProperty("Mobile: +1 (555) 234-5678")
    status_toast = StringProperty("")
    selected_relation = StringProperty("Spouse")
    is_active = BooleanProperty(True)
    automated_sos_markup = StringProperty(
        "[b][color=0B1C30]Automated SOS Protocol[/color][/b]\n"
        "[size=11sp][color=45464D]When SOS is triggered, an SMS alert with your real-time location link will automatically be sent to this person.[/color][/size]"
    )
    intro_markup = StringProperty(
        "[b][size=20sp][color=0B1C30]Emergency Contact[/color][/size][/b]\n"
        "[size=13sp][color=45464D]Set up your one trusted primary contact for SOS alerts[/color][/size]"
    )


    def on_enter(self):
        self.load_contact()

    def load_contact(self):
        """Populate UI from saved primary contact."""
        primary = get_primary_contact()
        if primary:
            name = primary.get("name", "Sarah Jenkins")
            self.guardian_name = name
            words = [w for w in name.split() if w]
            self.guardian_initials = (
                "".join([w[0].upper() for w in words[:2]]) if words else "EM"
            )
            rel = primary.get("relationship", "Spouse")
            self.guardian_relation = rel
            self.selected_relation = rel
            phone = primary.get("phone", "+1 (555) 234-5678")
            self.guardian_phone = f"Mobile: {phone}"

            if hasattr(self.ids, "name_field"):
                self.ids.name_field.text = name
            if hasattr(self.ids, "phone_field"):
                self.ids.phone_field.text = phone
        else:
            self.guardian_name = "No Contact Saved"
            self.guardian_initials = "--"
            self.guardian_relation = "None"
            self.guardian_phone = "Please configure a contact below"

    def select_relation(self, relation_name: str):
        """Handle relationship pill toggle (Parent, Spouse, Sibling, Friend)."""
        self.selected_relation = relation_name

    def save_contact(self):
        """Save contact details entered in form."""
        name = self.ids.name_field.text.strip()
        phone = self.ids.phone_field.text.strip()
        rel = self.selected_relation or "Spouse"

        if not name:
            self.show_toast("Please provide the contact's name.")
            return

        digits_only = "".join([c for c in phone if c.isdigit()])
        if len(digits_only) < 7:
            self.show_toast("Please provide a valid phone number (min 7 digits).")
            return

        save_or_update_contact(
            name=name,
            phone=phone,
            relationship=rel,
            is_enabled=True,
            is_primary=True,
        )

        self.load_contact()
        self.show_toast("Primary contact updated & armed successfully.")

        # Update home screen immediately
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, "sm") and app.sm.has_screen("home"):
            app.sm.get_screen("home").refresh()

    def test_alert(self):
        """Send a test SMS verification alert to the primary contact."""
        primary = get_primary_contact()
        if not primary or not primary.get("phone"):
            self.show_toast("No valid contact phone to test.")
            return

        # Check SEND_SMS runtime permission first
        try:
            from native_platform.native_bridge import check_permission, request_sms_permission
            if not check_permission("SEND_SMS"):
                self.show_toast("Requesting SMS permission...")
                request_sms_permission(lambda p, r: self._after_sms_perm(p, r))
                return
        except Exception:
            pass

        self._dispatch_test_sms()

    def _after_sms_perm(self, perms, results):
        if any(results):
            self._dispatch_test_sms()
        else:
            self.show_toast("SMS permission denied. Cannot send test SMS.")

    def _dispatch_test_sms(self):
        primary = get_primary_contact()
        if not primary:
            return
        from kivy.app import App
        app = App.get_running_app()
        msg = "ALERTX TEST: This is a test emergency alert from AlertX. Your contact is verified."
        res = app.sms.send(primary["phone"], msg)

        if res.get("ok"):
            self.show_toast("Sample test alert SMS dispatched.")
        else:
            self.show_toast(f"Test alert: {res.get('message', 'SMS failed')}")

    def show_toast(self, message: str):
        """Display feedback message."""
        self.status_toast = message
        Clock.schedule_once(lambda dt: self._clear_toast(), 3.5)

    def _clear_toast(self):
        self.status_toast = ""
