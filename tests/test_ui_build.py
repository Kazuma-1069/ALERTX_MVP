import os
import sys
from pathlib import Path

# Ensure app is on path
APP_DIR = Path(__file__).resolve().parent.parent / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Use headless/dummy window for testing without displaying full GUI
os.environ["KIVY_NO_ARGS"] = "1"

import pytest
from app.main import AlertXApp


def test_app_build_and_navigation():
    app = AlertXApp()
    sm = app.build()

    assert sm is not None
    assert sm.has_screen("home")
    assert sm.has_screen("contacts")
    assert sm.has_screen("safety")
    assert sm.has_screen("emergency")

    # Verify home screen properties
    home = sm.get_screen("home")
    home.refresh()
    assert "Sarah Jenkins" in home.contact_name or "No contact" in home.contact_name

    # Test navigation to contacts
    app.go_contacts()
    assert sm.current == "contacts"
    contacts_screen = sm.get_screen("contacts")
    contacts_screen.load_contact()
    assert contacts_screen.guardian_name != ""

    # Test navigation to safety
    app.go_safety()
    assert sm.current == "safety"

    # Test navigation to home
    app.go_home()
    assert sm.current == "home"

    # Test emergency activation
    app.start_emergency()
    assert sm.current == "emergency"
    emergency_screen = sm.get_screen("emergency")
    assert emergency_screen.session_id.startswith("AX-")
    assert emergency_screen.timer_text.startswith("Active")

    # Test emergency cancellation
    emergency_screen.cancel_emergency()
    assert sm.current == "home"
