import pytest
from app.services.location import LocationService
from app.services.sms import SmsService
from app.services.calling import CallingService
from app.services.emergency import (
    EmergencyService,
    load_contacts,
    save_or_update_contact,
    get_primary_contact,
    delete_contact,
    toggle_contact_enabled,
)


def test_location_service_maps_url_and_formatting():
    service = LocationService()
    url = service.generate_maps_url(37.774929, -122.419416)
    assert "https://maps.google.com/?q=37.774929,-122.419416" == url

    coords = service.format_coordinates(37.7749, -122.4194)
    assert "37.7749° N, 122.4194° W" == coords

    # Without fix, must NOT return fake coordinates
    cur = service.get_current()
    if not cur["ok"]:
        assert cur["coordinates_str"] == "Unable to obtain current location"
        assert cur["lat"] is None


def test_location_mock_for_testing():
    service = LocationService()
    service.set_mock_location_for_testing(34.0522, -118.2437, accuracy=4.1)
    cur = service.get_current()
    assert cur["ok"] is True
    assert cur["lat"] == 34.0522
    assert cur["lon"] == -118.2437
    assert "Within ±4.1 meters" in cur["accuracy_str"]
    assert "https://maps.google.com/?q=34.052200,-118.243700" == cur["maps_url"]


def test_sms_service_desktop_behavior():
    sms = SmsService()
    # On desktop, must cleanly report unavailable without pretending success
    res = sms.send("+15551234567", "Test alert")
    assert res["ok"] is False
    assert "SMS unavailable" in res["message"]


def test_calling_service_desktop_behavior():
    calling = CallingService()
    res = calling.call("+15551234567")
    assert res["ok"] is False
    assert "unavailable on desktop" in res["message"]


def test_contact_management_and_persistence():
    save_or_update_contact(
        name="John Doe",
        phone="+15559876543",
        relationship="Parent",
        is_enabled=True,
        is_primary=True,
        contact_id="test_c1",
    )

    primary = get_primary_contact()
    assert primary is not None
    assert primary["name"] == "John Doe"
    assert primary["relationship"] == "Parent"

    # Toggle enabled
    toggled = toggle_contact_enabled("test_c1")
    assert toggled is False

    # Toggle back
    toggled = toggle_contact_enabled("test_c1")
    assert toggled is True

    # Clean up test contact
    delete_contact("test_c1")


def test_emergency_orchestration_workflow():
    loc = LocationService()
    loc.set_mock_location_for_testing(37.7749, -122.4194, accuracy=3.2)

    sms = SmsService()
    sms.enable_test_mode_for_unit_tests()

    calling = CallingService()
    calling.enable_test_mode_for_unit_tests()

    emergency = EmergencyService(loc, sms, calling)

    # Ensure a contact exists
    save_or_update_contact(
        name="Sarah Jenkins",
        phone="+15552345678",
        relationship="Spouse",
        is_enabled=True,
        is_primary=True,
        contact_id="test_sarah",
    )

    res = emergency.activate()
    assert res["ok"] is True
    assert res["status"] == "EMERGENCY ACTIVE"
    assert res["session_id"].startswith("AX-")
    assert "maps.google.com" in res["dispatched_payload"]
    assert res["sms_status"] == "Delivered"
    assert "Calling" in res["call_status"]

    # Verify cancel
    cancel_res = emergency.cancel()
    assert cancel_res["status"] == "cancelled"
    assert emergency.active_session is None

    # Cleanup
    delete_contact("test_sarah")
