"""AlertX Safety & Settings Screen.

Allows configuring SOS alert message template, emergency broadcast
preferences, and viewing hardware permissions and diagnostics.
"""

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from services.emergency import load_contacts, get_primary_contact, DEFAULT_SOS_MESSAGE_TEMPLATE


class SettingsScreen(Screen):
    status_text = StringProperty("")
    message_preview = StringProperty("")
    gps_status_text = StringProperty("GPS Location Receiver: Ready (High Accuracy)")
    sms_status_text = StringProperty("Cellular SMS Telephony: Active")
    call_status_text = StringProperty("Emergency Calling Dispatch: Armed")
    cloud_status_text = StringProperty("Cloud Backend Sync: Standalone Mode")

    def on_enter(self):
        self.refresh()

    def refresh(self):
        from kivy.app import App
        app = App.get_running_app()
        raw = app.emergency.message_template.format(
            maps_url="https://maps.google.com/?q=37.7749,-122.4194"
        )
        self.message_preview = raw.replace("🚨 ", "")

        # Dynamic permission diagnostics
        try:
            from native_platform.native_bridge import get_permission_diagnostics, is_android
            if is_android():
                diag = get_permission_diagnostics()
                has_loc = diag.get("ACCESS_FINE_LOCATION") or diag.get("ACCESS_COARSE_LOCATION")
                has_sms = diag.get("SEND_SMS")
                has_call = diag.get("CALL_PHONE")

                self.gps_status_text = f"GPS Location: {'Granted (High Precision)' if has_loc else 'Permission Denied / Missing'}"
                self.sms_status_text = f"Cellular SMS: {'Granted (Carrier Uplink Ready)' if has_sms else 'Permission Denied / Missing'}"
                self.call_status_text = f"Voice Calling: {'Granted (Direct Call Armed)' if has_call else 'Dialer Fallback Mode'}"
            else:
                self.gps_status_text = "GPS Location: Ready (Desktop Simulator)"
                self.sms_status_text = "Cellular SMS: Simulated (Desktop Mode)"
                self.call_status_text = "Voice Calling: Simulated (Desktop Mode)"
        except Exception:
            pass

        # Dynamic Cloud Backend check
        if hasattr(app, "api") and app.api:
            if app.api.is_online:
                self.cloud_status_text = "Cloud Backend: Connected (Live Telemetry Sync)"
            else:
                self.cloud_status_text = "Cloud Backend: Standalone Safety Mode (Local Active)"

        self.status_text = "Diagnostics & settings synchronized."

    def reset_template(self):
        from kivy.app import App
        app = App.get_running_app()
        app.emergency.message_template = DEFAULT_SOS_MESSAGE_TEMPLATE
        self.refresh()
        self.status_text = "SOS message restored to default."

    def request_all_permissions(self):
        """Prompt user for missing Android runtime permissions."""
        try:
            from native_platform.native_bridge import request_emergency_permissions
            request_emergency_permissions(lambda perms, results: self.refresh())
        except Exception as exc:
            self.status_text = f"Permission error: {exc}"

