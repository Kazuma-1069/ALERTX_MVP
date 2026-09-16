"""AlertX Native Android Bridge.

Provides runtime permissions management and platform diagnostics for real
Android devices while remaining fail-safe on desktop/emulator environments.
"""

from kivy.utils import platform

IS_ANDROID = platform == "android"


def is_android() -> bool:
    """Return True if running on a real Android device/runtime."""
    return IS_ANDROID


def request_emergency_permissions(callback=None):
    """Request all runtime permissions required for emergency SOS.

    Required permissions:
    - ACCESS_FINE_LOCATION: Real GPS fixes with meters accuracy
    - ACCESS_COARSE_LOCATION: Cellular/Wi-Fi assisted positioning
    - SEND_SMS: Dispatching emergency messages via cellular network
    - CALL_PHONE: Initiating direct emergency phone call to primary contact
    """
    if not IS_ANDROID:
        if callback:
            callback(["android.permission.SEND_SMS"], [True])
        return

    try:
        from android.permissions import Permission, request_permissions

        permissions = [
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION,
            Permission.SEND_SMS,
            Permission.CALL_PHONE,
        ]

        def _on_permissions(perms, results):
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and hasattr(app, "location"):
                    app.location.start_gps()
            except Exception:
                pass
            if callback:
                callback(perms, results)

        request_permissions(permissions, _on_permissions)
    except Exception as exc:
        print(f"[AlertX Bridge] Permission request failed: {exc}")
        if callback:
            callback([], [])


def check_permission(perm_name: str) -> bool:
    """Check whether an Android runtime permission has been granted."""
    if not IS_ANDROID:
        return True

    try:
        from android.permissions import Permission, check_permission as _check

        perm_enum = getattr(Permission, perm_name, perm_name)
        return _check(perm_enum)
    except Exception:
        return False
