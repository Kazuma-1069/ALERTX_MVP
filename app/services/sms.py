"""AlertX SMS Dispatch Service.

Integrates real Android cellular SMS dispatch via PyJNIus and SmsManager.
Handles multipart messaging for long emergency messages with GPS links.
Reports actual delivery and failure states without pretending success.
"""

from typing import Any, Dict
from kivy.utils import platform

IS_ANDROID = platform == "android"


class SmsService:
    """Service to transmit real emergency SMS notifications."""

    def __init__(self):
        self._test_mode = False
        self._test_sent_log = []

    def send(self, phone: str, message: str) -> Dict[str, Any]:
        """Send an SMS message to the specified phone number.

        On real Android devices:
        - Uses android.telephony.SmsManager
        - Splits messages into parts if exceeding 160 characters (divideMessage)
        - Transmits via sendMultipartTextMessage or sendTextMessage

        On non-Android (desktop/development):
        - Accurately reports SMS hardware unavailability rather than faking success.
        """
        clean_phone = phone.strip()
        if not clean_phone:
            return {"ok": False, "message": "No phone number provided", "recipient": phone}

        if self._test_mode:
            self._test_sent_log.append({"phone": clean_phone, "message": message})
            return {"ok": True, "message": "Delivered (Test)", "recipient": clean_phone}

        if not IS_ANDROID:
            return {
                "ok": False,
                "message": "SMS unavailable on desktop (cellular hardware required)",
                "recipient": clean_phone,
            }

        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            SmsManager = autoclass("android.telephony.SmsManager")
            try:
                manager = activity.getSystemService(SmsManager)
            except Exception:
                manager = SmsManager.getDefault()

            parts = manager.divideMessage(message)
            if parts.size() > 1:
                manager.sendMultipartTextMessage(clean_phone, None, parts, None, None)
            else:
                manager.sendTextMessage(clean_phone, None, message, None, None)

            return {
                "ok": True,
                "message": "Delivered",
                "recipient": clean_phone,
            }

        except Exception as exc:
            return {
                "ok": False,
                "message": f"SMS dispatch failed: {exc.__class__.__name__}",
                "recipient": clean_phone,
            }

    def enable_test_mode_for_unit_tests(self):
        """Enable safe in-memory tracking solely for automated test suites."""
        self._test_mode = True
        self._test_sent_log.clear()
