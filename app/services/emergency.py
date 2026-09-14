"""AlertX Emergency Orchestration & Contact Management Service.

Coordinates real-time emergency dispatch across:
- Real GPS positioning
- Cellular SMS dispatch
- Telephony voice calling
- Persistent multi-contact management with enable/disable states
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

CONTACTS_FILE = Path(__file__).resolve().parent.parent / "contact.json"

DEFAULT_SOS_MESSAGE_TEMPLATE = "🚨 ALERTX EMERGENCY ALERT: I need immediate help. Location: {maps_url}"


def load_contacts() -> List[Dict[str, Any]]:
    """Load all contacts from local storage.

    Ensures backward compatibility with single-contact schemas.
    """
    if not CONTACTS_FILE.exists():
        # Initialize with Stitch design default contact
        initial = [
            {
                "id": "c_default_1",
                "name": "Sarah Jenkins",
                "phone": "+1 (555) 234-5678",
                "relationship": "Spouse",
                "is_enabled": True,
                "is_primary": True,
            }
        ]
        save_all_contacts(initial)
        return initial

    try:
        data = json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            # Migrate legacy single contact dict
            migrated = [
                {
                    "id": "c_1",
                    "name": data.get("name", "Emergency Contact"),
                    "phone": data.get("phone", ""),
                    "relationship": data.get("relationship", "Other"),
                    "is_enabled": True,
                    "is_primary": True,
                }
            ]
            save_all_contacts(migrated)
            return migrated
    except Exception as exc:
        print(f"[AlertX Contacts] Failed to read contacts: {exc}")

    return []


def save_all_contacts(contacts: List[Dict[str, Any]]):
    """Persist contact list to local JSON file."""
    CONTACTS_FILE.write_text(json.dumps(contacts, indent=2), encoding="utf-8")


def get_primary_contact() -> Optional[Dict[str, Any]]:
    """Return the primary enabled contact, or the first contact."""
    contacts = load_contacts()
    for c in contacts:
        if c.get("is_primary") and c.get("is_enabled", True):
            return c
    for c in contacts:
        if c.get("is_enabled", True):
            return c
    return contacts[0] if contacts else None


def save_or_update_contact(
    name: str,
    phone: str,
    relationship: str = "Spouse",
    is_enabled: bool = True,
    is_primary: bool = True,
    contact_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Add a new contact or update an existing one."""
    contacts = load_contacts()
    clean_name = name.strip()
    clean_phone = phone.strip()

    if is_primary:
        for c in contacts:
            c["is_primary"] = False

    if not contact_id:
        contact_id = f"c_{uuid4().hex[:8]}"
        contact_entry = {
            "id": contact_id,
            "name": clean_name,
            "phone": clean_phone,
            "relationship": relationship,
            "is_enabled": is_enabled,
            "is_primary": is_primary,
        }
        contacts.insert(0, contact_entry)
    else:
        found = False
        for c in contacts:
            if c.get("id") == contact_id:
                c["name"] = clean_name
                c["phone"] = clean_phone
                c["relationship"] = relationship
                c["is_enabled"] = is_enabled
                c["is_primary"] = is_primary
                found = True
                break
        if not found:
            contact_entry = {
                "id": contact_id,
                "name": clean_name,
                "phone": clean_phone,
                "relationship": relationship,
                "is_enabled": is_enabled,
                "is_primary": is_primary,
            }
            contacts.insert(0, contact_entry)

    save_all_contacts(contacts)
    return get_primary_contact() or {}


def delete_contact(contact_id: str):
    """Delete a contact by ID."""
    contacts = [c for c in load_contacts() if c.get("id") != contact_id]
    if contacts and not any(c.get("is_primary") for c in contacts):
        contacts[0]["is_primary"] = True
    save_all_contacts(contacts)


def toggle_contact_enabled(contact_id: str) -> bool:
    """Toggle a contact's enabled state."""
    contacts = load_contacts()
    new_state = True
    for c in contacts:
        if c.get("id") == contact_id:
            c["is_enabled"] = not c.get("is_enabled", True)
            new_state = c["is_enabled"]
            break
    save_all_contacts(contacts)
    return new_state


# Backward compatibility aliases
def load_contact():
    return get_primary_contact()


def save_contact(name, phone, relationship="Spouse"):
    return save_or_update_contact(name, phone, relationship, is_enabled=True, is_primary=True)


class EmergencyService:
    """Full lifecycle orchestrator for AlertX emergency responses."""

    def __init__(self, location_service, sms_service, calling_service=None):
        self.location = location_service
        self.sms = sms_service
        self.calling = calling_service
        self.active_session: Optional[Dict[str, Any]] = None
        self.message_template = DEFAULT_SOS_MESSAGE_TEMPLATE

    def activate(self) -> Dict[str, Any]:
        """Trigger the complete emergency dispatch workflow.

        Steps:
        1. Obtain real GPS location
        2. Retrieve enabled emergency contacts
        3. Compose payload with location link
        4. Send real SMS to enabled contacts
        5. Initiate real phone call to primary contact
        6. Return complete dispatch state
        """
        session_id = f"AX-{uuid4().hex[:4].upper()}"
        start_time_str = datetime.now().strftime("%I:%M %p")
        enabled_contacts = [c for c in load_contacts() if c.get("is_enabled", True)]
        primary = get_primary_contact()

        if not enabled_contacts:
            result = {
                "ok": False,
                "session_id": session_id,
                "start_time": start_time_str,
                "status": "No Contact Configured",
                "location_status": "Not Requested",
                "coordinates": "Add and enable an emergency contact first.",
                "accuracy_str": "—",
                "sms_status": "SMS not sent (No enabled contact)",
                "call_status": "Calling not initiated",
                "recipient": "None",
                "dispatched_payload": "No contact configured",
            }
            self.active_session = result
            return result

        # 1. Real GPS location
        loc = self.location.get_current()
        if loc.get("ok"):
            maps_url = loc["maps_url"]
            location_status = loc["status"]
            coordinates_str = loc["coordinates_str"]
            accuracy_str = loc["accuracy_str"]
        else:
            maps_url = "Location unavailable (GPS offline)"
            location_status = "Unavailable"
            coordinates_str = "Unable to obtain current location"
            accuracy_str = "No satellite lock"

        # 2. Format SOS message
        message = self.message_template.format(maps_url=maps_url)

        # 3. Send SMS to enabled contacts
        sms_results = []
        for contact in enabled_contacts:
            res = self.sms.send(contact["phone"], message)
            sms_results.append(res)

        from kivy.utils import platform
        is_android_device = platform == "android"

        sms_success_count = sum(1 for r in sms_results if r.get("ok"))
        if sms_success_count == len(enabled_contacts) and sms_success_count > 0:
            sms_status = "Delivered"
        elif sms_success_count > 0:
            sms_status = f"Delivered ({sms_success_count}/{len(enabled_contacts)})"
        else:
            sms_status = "Failed" if is_android_device else "Offline (Dev)"

        # 4. Initiate Emergency Calling to primary contact
        call_status = "Dialer Ready"
        if self.calling and primary:
            call_res = self.calling.call(primary["phone"])
            if call_res.get("ok"):
                call_status = f"Calling {primary.get('name', 'Contact')}"
            else:
                call_status = "Calling Failed" if is_android_device else "Offline (Dev)"

        primary_name = primary.get("name", "Contact") if primary else "Contact"
        primary_phone = primary.get("phone", "") if primary else ""

        result = {
            "ok": True,
            "session_id": session_id,
            "start_time": start_time_str,
            "status": "EMERGENCY ACTIVE",
            "location_status": location_status,
            "coordinates": coordinates_str,
            "accuracy_str": accuracy_str,
            "sms_status": sms_status,
            "call_status": call_status,
            "recipient_name": primary_name,
            "recipient_phone": primary_phone,
            "recipient": f"{primary_name} • {primary_phone}",
            "dispatched_payload": message,
            "created_at": time.time(),
        }

        self.active_session = result
        return result

    def cancel(self) -> Dict[str, Any]:
        """Cancel and deactivate the emergency dispatch."""
        prev = self.active_session
        self.active_session = None
        return {"status": "cancelled", "previous_session": prev}
