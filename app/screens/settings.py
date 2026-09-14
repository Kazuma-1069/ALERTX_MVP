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

    def on_enter(self):
        self.refresh()

    def refresh(self):
        from kivy.app import App
        app = App.get_running_app()
        raw = app.emergency.message_template.format(
            maps_url="https://maps.google.com/?q=37.7749,-122.4194"
        )
        self.message_preview = raw.replace("🚨 ", "")
        self.status_text = "Settings synchronized."

    def reset_template(self):
        from kivy.app import App
        app = App.get_running_app()
        app.emergency.message_template = DEFAULT_SOS_MESSAGE_TEMPLATE
        self.refresh()
        self.status_text = "SOS message restored to default."
