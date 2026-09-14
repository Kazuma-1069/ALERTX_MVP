import os
import sys
from pathlib import Path

# Add app directory
APP_DIR = Path(__file__).resolve().parent / "app"
sys.path.insert(0, str(APP_DIR))

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '840')
Config.set('graphics', 'resizable', '0')

from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition
from app.main import AlertXApp

OUTPUT_DIR = Path(__file__).resolve().parent / "rendered_screens"
OUTPUT_DIR.mkdir(exist_ok=True)


class ScreenshotApp(AlertXApp):
    def build(self):
        sm = super().build()
        sm.transition = NoTransition()
        self.location.set_mock_location_for_testing(37.7749, -122.4194, accuracy=3.2)
        Clock.schedule_once(self.step_home, 1.0)
        return sm

    def step_home(self, dt):
        self.go_home()
        Clock.schedule_once(self._capture_home, 0.5)

    def _capture_home(self, dt):
        self.root.export_to_png(str(OUTPUT_DIR / "home.png"))
        print("Captured Home screen via export_to_png")
        Clock.schedule_once(self.step_contacts, 0.6)

    def step_contacts(self, dt):
        self.go_contacts()
        Clock.schedule_once(self._capture_contacts, 0.5)

    def _capture_contacts(self, dt):
        self.root.export_to_png(str(OUTPUT_DIR / "contacts.png"))
        print("Captured Contacts screen via export_to_png")
        Clock.schedule_once(self.step_emergency, 0.6)

    def step_emergency(self, dt):
        self.start_emergency()
        Clock.schedule_once(self._capture_emergency, 0.5)

    def _capture_emergency(self, dt):
        self.root.export_to_png(str(OUTPUT_DIR / "emergency.png"))
        print("Captured Emergency screen via export_to_png")
        Clock.schedule_once(self.step_safety, 0.6)

    def step_safety(self, dt):
        self.go_safety()
        Clock.schedule_once(self._capture_safety, 0.5)

    def _capture_safety(self, dt):
        self.root.export_to_png(str(OUTPUT_DIR / "safety.png"))
        print("Captured Safety screen via export_to_png")
        Clock.schedule_once(self.finish, 0.6)

    def finish(self, dt):
        print("All screenshots captured successfully via export_to_png!")
        self.stop()


if __name__ == "__main__":
    ScreenshotApp().run()
