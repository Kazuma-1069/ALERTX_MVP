"""AlertX Emergency Calling Service.

Integrates real Android telephony calling via PyJNIus and Android Intents.
Uses Intent.ACTION_CALL when CALL_PHONE permission is granted, and
gracefully falls back to Intent.ACTION_DIAL when restricted by OS policies.
Reports authentic calling dispatch states without faking success.
"""

from typing import Any, Dict
from kivy.utils import platform

IS_ANDROID = platform == "android"


class CallingService:
    """Service to initiate native emergency voice calls."""

    def __init__(self):
        self._test_mode = False
        self._test_call_log = []

    def call(self, phone: str) -> Dict[str, Any]:
        """Initiate an emergency voice call to the given phone number.

        On real Android devices:
        - Creates an Intent with ACTION_CALL
        - If CALL_PHONE permission is withheld, falls back to ACTION_DIAL
        - Dispatches via current PythonActivity

        On non-Android environments:
        - Accurately reports telephony unavailability.
        """
        clean_phone = phone.strip().replace(" ", "").replace("-", "")
        if not clean_phone:
            return {"ok": False, "message": "No phone number provided", "recipient": phone}

        if self._test_mode:
            self._test_call_log.append(clean_phone)
            return {"ok": True, "message": f"Calling (Test) {clean_phone}", "recipient": clean_phone}

        if not IS_ANDROID:
            return {
                "ok": False,
                "message": "Phone calling unavailable on desktop",
                "recipient": clean_phone,
            }

        try:
            from jnius import autoclass

            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            activity = PythonActivity.mActivity

            # First attempt direct call (ACTION_CALL)
            try:
                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(f"tel:{clean_phone}"))
                activity.startActivity(intent)
                return {
                    "ok": True,
                    "message": f"Calling {clean_phone}...",
                    "recipient": clean_phone,
                }
            except Exception:
                # Fallback to ACTION_DIAL if CALL_PHONE is restricted
                dial_intent = Intent(Intent.ACTION_DIAL)
                dial_intent.setData(Uri.parse(f"tel:{clean_phone}"))
                activity.startActivity(dial_intent)
                return {
                    "ok": True,
                    "message": f"Dialer Opened for {clean_phone}",
                    "recipient": clean_phone,
                }

        except Exception as exc:
            return {
                "ok": False,
                "message": f"Calling failed: {exc.__class__.__name__}",
                "recipient": clean_phone,
            }

    def enable_test_mode_for_unit_tests(self):
        """Enable safe in-memory call tracking for test suites."""
        self._test_mode = True
        self._test_call_log.clear()
