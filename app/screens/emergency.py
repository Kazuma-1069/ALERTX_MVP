"""AlertX Emergency Active Screen.

Displays real-time crisis dispatch telemetry, including active session ID,
real GPS coordinates, SMS transmission status, live elapsed timer,
and failsafe cancellation controls.
Follows Stitch Guardian Modern design system.
"""

from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen


class EmergencyScreen(Screen):
    session_id = StringProperty("AX-8921")
    start_time_text = StringProperty("09:42 AM")
    location_status = StringProperty("High Precision")
    coordinates = StringProperty("37.7749° N, 122.4194° W")
    accuracy_str = StringProperty("Within ±3.2 meters")
    sms_badge = StringProperty("Delivered")
    sms_payload = StringProperty("EMERGENCY! I need immediate help.")
    sms_payload_markup = StringProperty(
        "[b][size=9sp][color=45464D]DISPATCHED PAYLOAD[/color][/size][/b]\n"
        "[i][size=11sp][color=0B1C30]EMERGENCY! I need immediate help.[/color][/size][/i]"
    )
    recipient_name = StringProperty("Sarah Jenkins")
    recipient_initials = StringProperty("SJ")
    recipient_phone = StringProperty("+1 555-234-5678")
    call_status = StringProperty("Calling Dispatched")
    timer_text = StringProperty("Active 00:00")
    is_active = BooleanProperty(True)

    elapsed_seconds = NumericProperty(0)
    _timer_event = None

    def on_enter(self):
        self.start_timer()

    def on_leave(self):
        self.stop_timer()

    def start_timer(self):
        self.stop_timer()
        self.elapsed_seconds = 0
        self._update_timer_display()
        self._timer_event = Clock.schedule_interval(self._tick_timer, 1.0)

    def stop_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None

    def _tick_timer(self, dt):
        self.elapsed_seconds += 1
        self._update_timer_display()

    def _update_timer_display(self):
        hours = int(self.elapsed_seconds // 3600)
        mins = int((self.elapsed_seconds % 3600) // 60)
        secs = int(self.elapsed_seconds % 60)
        if hours > 0:
            self.timer_text = f"Active {hours:02d}:{mins:02d}:{secs:02d}"
        else:
            self.timer_text = f"Active {mins:02d}:{secs:02d}"

    def apply_result(self, result: dict):
        """Apply dispatch result from EmergencyService."""
        self.session_id = result.get("session_id", "AX-8921")
        self.start_time_text = result.get("start_time", "Just now")
        self.location_status = result.get("location_status", "Acquired")
        self.coordinates = result.get("coordinates", "Unable to obtain current location")
        self.accuracy_str = result.get("accuracy_str", "—")
        self.sms_badge = result.get("sms_status", "Dispatched")
        self.sms_payload = result.get("dispatched_payload", "Emergency alert dispatched.")
        clean_payload = self.sms_payload.replace("🚨 ", "")
        self.sms_payload_markup = (
            f"[b][size=9sp][color=45464D]DISPATCHED PAYLOAD[/color][/size][/b]\n"
            f"[i][size=11sp][color=0B1C30]{clean_payload}[/color][/size][/i]"
        )

        name = result.get("recipient_name", "Sarah Jenkins")
        self.recipient_name = name
        words = [w for w in name.split() if w]
        self.recipient_initials = (
            "".join([w[0].upper() for w in words[:2]]) if words else "EM"
        )
        self.recipient_phone = result.get("recipient_phone", "+1 (555) 234-5678")
        self.call_status = result.get("call_status", "Calling...")
        self.start_timer()

    def cancel_emergency(self):
        """Cancel the emergency alert and return to home screen."""
        self.stop_timer()
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, "emergency"):
            app.emergency.cancel()
        app.go_home()
