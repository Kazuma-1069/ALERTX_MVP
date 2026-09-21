"""AlertX Native Android Bridge.

Provides runtime permissions management and platform diagnostics for real
Android devices while remaining fail-safe on desktop/emulator environments.
Never crashes on denial, always synchronizes callbacks to Kivy's main thread.
"""

import os
from typing import Any, Callable, Dict, List, Optional

try:
    from kivy.utils import platform
    IS_ANDROID = platform == "android"
except ImportError:
    IS_ANDROID = "ANDROID_ARGUMENT" in os.environ or "ANDROID_ROOT" in os.environ


def is_android() -> bool:
    """Return True if running on a real Android device/runtime."""
    return IS_ANDROID


def _normalize_permission(perm_name: str) -> str:
    """Ensure permission string includes android.permission prefix."""
    if perm_name.startswith("android.permission."):
        return perm_name
    return f"android.permission.{perm_name}"


def check_permission(perm_name: str) -> bool:
    """Check whether an Android runtime permission has been granted."""
    if not IS_ANDROID:
        return True

    full_perm = _normalize_permission(perm_name)

    # 1. Try python-for-android wrapper
    try:
        from android.permissions import Permission, check_permission as _check
        short_name = perm_name.replace("android.permission.", "")
        perm_target = getattr(Permission, short_name, full_perm)
        if _check(perm_target):
            return True
    except Exception:
        pass

    # 2. Resilient fallback via PyJNIus ContextCompat / Activity
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        activity = PythonActivity.mActivity
        if activity:
            PackageManager = autoclass("android.content.pm.PackageManager")
            res = activity.checkSelfPermission(full_perm)
            return res == PackageManager.PERMISSION_GRANTED
    except Exception:
        pass

    return False


def get_permission_diagnostics() -> Dict[str, bool]:
    """Return granted status for all required AlertX permissions."""
    if not IS_ANDROID:
        return {
            "ACCESS_FINE_LOCATION": True,
            "ACCESS_COARSE_LOCATION": True,
            "SEND_SMS": True,
            "CALL_PHONE": True,
        }
    return {
        "ACCESS_FINE_LOCATION": check_permission("ACCESS_FINE_LOCATION"),
        "ACCESS_COARSE_LOCATION": check_permission("ACCESS_COARSE_LOCATION"),
        "SEND_SMS": check_permission("SEND_SMS"),
        "CALL_PHONE": check_permission("CALL_PHONE"),
    }


def get_missing_permissions() -> List[str]:
    """Return list of required permissions not yet granted."""
    if not IS_ANDROID:
        return []

    required = ["ACCESS_FINE_LOCATION", "SEND_SMS", "CALL_PHONE"]
    missing = []
    for p in required:
        if not check_permission(p):
            if p == "ACCESS_FINE_LOCATION" and check_permission("ACCESS_COARSE_LOCATION"):
                continue
            missing.append(p)
    return missing


def has_all_emergency_permissions() -> bool:
    """Return True if all essential emergency permissions are granted."""
    return len(get_missing_permissions()) == 0


def _safe_dispatch_callback(callback: Optional[Callable], perms: List[str], results: List[bool]):
    """Schedule callback execution on Kivy's main thread to avoid Looper thread collisions."""
    if not callback:
        return
    try:
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: callback(perms, results), 0)
    except Exception:
        try:
            callback(perms, results)
        except Exception:
            pass


def request_location_permissions(callback: Optional[Callable] = None):
    """Request runtime location permissions safely."""
    if not IS_ANDROID:
        _safe_dispatch_callback(callback, ["android.permission.ACCESS_FINE_LOCATION"], [True])
        return

    # Check if already granted first to avoid disruptive prompts
    if check_permission("ACCESS_FINE_LOCATION") or check_permission("ACCESS_COARSE_LOCATION"):
        _safe_dispatch_callback(callback, ["android.permission.ACCESS_FINE_LOCATION"], [True])
        return

    try:
        from android.permissions import Permission, request_permissions

        def _on_result(perms, results):
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and hasattr(app, "location") and any(results):
                    app.location.start_gps()
            except Exception:
                pass
            _safe_dispatch_callback(callback, perms, results)

        request_permissions([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION], _on_result)
    except Exception as exc:
        print(f"[AlertX Bridge] Location permission request error: {exc}")
        _safe_dispatch_callback(callback, [], [])


def request_sms_permission(callback: Optional[Callable] = None):
    """Request runtime SMS sending permission safely."""
    if not IS_ANDROID:
        _safe_dispatch_callback(callback, ["android.permission.SEND_SMS"], [True])
        return

    if check_permission("SEND_SMS"):
        _safe_dispatch_callback(callback, ["android.permission.SEND_SMS"], [True])
        return

    try:
        from android.permissions import Permission, request_permissions

        def _on_result(perms, results):
            _safe_dispatch_callback(callback, perms, results)

        request_permissions([Permission.SEND_SMS], _on_result)
    except Exception as exc:
        print(f"[AlertX Bridge] SMS permission request error: {exc}")
        _safe_dispatch_callback(callback, [], [])


def request_call_permission(callback: Optional[Callable] = None):
    """Request runtime Phone Calling permission safely."""
    if not IS_ANDROID:
        _safe_dispatch_callback(callback, ["android.permission.CALL_PHONE"], [True])
        return

    if check_permission("CALL_PHONE"):
        _safe_dispatch_callback(callback, ["android.permission.CALL_PHONE"], [True])
        return

    try:
        from android.permissions import Permission, request_permissions

        def _on_result(perms, results):
            _safe_dispatch_callback(callback, perms, results)

        request_permissions([Permission.CALL_PHONE], _on_result)
    except Exception as exc:
        print(f"[AlertX Bridge] Calling permission request error: {exc}")
        _safe_dispatch_callback(callback, [], [])


def request_emergency_permissions(callback: Optional[Callable] = None):
    """Request all missing runtime permissions required for emergency SOS."""
    if not IS_ANDROID:
        _safe_dispatch_callback(
            callback,
            [
                "android.permission.ACCESS_FINE_LOCATION",
                "android.permission.ACCESS_COARSE_LOCATION",
                "android.permission.SEND_SMS",
                "android.permission.CALL_PHONE",
            ],
            [True, True, True, True],
        )
        return

    try:
        from android.permissions import Permission, request_permissions

        needed = []
        if not check_permission("ACCESS_FINE_LOCATION") and not check_permission("ACCESS_COARSE_LOCATION"):
            needed.extend([Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_COARSE_LOCATION])
        if not check_permission("SEND_SMS"):
            needed.append(Permission.SEND_SMS)
        if not check_permission("CALL_PHONE"):
            needed.append(Permission.CALL_PHONE)

        # If everything is already granted, avoid disruptive dialog
        if not needed:
            _safe_dispatch_callback(callback, [], [])
            return

        def _on_permissions(perms, results):
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and hasattr(app, "location") and any(results):
                    app.location.start_gps()
            except Exception:
                pass
            _safe_dispatch_callback(callback, perms, results)

        request_permissions(needed, _on_permissions)
    except Exception as exc:
        print(f"[AlertX Bridge] All permissions request notice: {exc}")
        _safe_dispatch_callback(callback, [], [])
