"""AlertX Backend API Client Service.

Provides resilient, non-blocking HTTP synchronization with the AlertX backend.
Works offline gracefully without blocking emergency operations.
Uses Python's standard urllib to guarantee compatibility across Android and desktop.
"""

import json
import os
import threading
from typing import Any, Callable, Dict, Optional
import urllib.error
import urllib.request
try:
    from utils.constants import API_BASE_URL
except ImportError:
    try:
        from app.utils.constants import API_BASE_URL
    except ImportError:
        API_BASE_URL = "http://10.0.2.2:8000"



class ApiService:
    """Client service for AlertX FastAPI backend."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (
            base_url
            or os.environ.get("ALERTX_API_URL")
            or API_BASE_URL
        ).rstrip("/")
        self.timeout = 3.0  # 3 seconds max timeout to prevent UI freezes
        self.is_online = False
        self._last_error = ""

    def _request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Synchronous resilient HTTP request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        req_headers = {"User-Agent": "AlertX-Mobile/0.1.0", "Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)

        body = None
        if data is not None:
            body = json.dumps(data).encode("utf-8")

        try:
            req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status_code = resp.status
                raw = resp.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                self.is_online = True
                self._last_error = ""
                return {"ok": True, "status_code": status_code, "data": parsed}
        except urllib.error.HTTPError as exc:
            err_body = ""
            try:
                err_body = exc.read().decode("utf-8")
            except Exception:
                pass
            self.is_online = True  # Server responded even if error
            self._last_error = f"HTTP {exc.code}"
            return {"ok": False, "status_code": exc.code, "error": f"HTTP {exc.code}", "detail": err_body}
        except Exception as exc:
            self.is_online = False
            self._last_error = str(exc)
            return {"ok": False, "offline": True, "error": str(exc)}

    def check_health(self) -> Dict[str, Any]:
        """Verify backend availability via GET /health."""
        res = self._request("GET", "/health")
        if res.get("ok") and res.get("data", {}).get("status") == "ok":
            self.is_online = True
            return {"ok": True, "status": "online", "service": res["data"].get("service", "ALERTX")}
        self.is_online = False
        return {"ok": False, "status": "offline", "error": res.get("error", "Unreachable")}

    def sync_contact(self, name: str, phone: str, relationship: str = "") -> Dict[str, Any]:
        """Persist or update contact on backend via POST /contacts."""
        payload = {"name": name.strip(), "phone": phone.strip(), "relationship": relationship.strip()}
        return self._request("POST", "/contacts", data=payload)

    def fetch_contact(self) -> Dict[str, Any]:
        """Retrieve configured contact from backend via GET /contacts."""
        return self._request("GET", "/contacts")

    def start_emergency_session(self) -> Dict[str, Any]:
        """Initiate an emergency session on backend via POST /emergency/start."""
        return self._request("POST", "/emergency/start")

    def update_emergency_location(
        self, session_id: str, latitude: float, longitude: float, accuracy: Optional[float] = None
    ) -> Dict[str, Any]:
        """Post GPS coordinates to active session via POST /emergency/{sid}/location."""
        payload = {"latitude": latitude, "longitude": longitude, "accuracy": accuracy}
        return self._request("POST", f"/emergency/{session_id}/location", data=payload)

    def complete_emergency_session(self, session_id: str) -> Dict[str, Any]:
        """Mark emergency session resolved on backend via POST /emergency/{sid}/complete."""
        return self._request("POST", f"/emergency/{session_id}/complete")

    # Asynchronous non-blocking wrappers
    def async_sync_contact(self, name: str, phone: str, relationship: str = "", callback: Optional[Callable] = None):
        def _worker():
            res = self.sync_contact(name, phone, relationship)
            if callback:
                callback(res)
        threading.Thread(target=_worker, daemon=True).start()

    def async_report_emergency(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        accuracy: Optional[float] = None,
        callback: Optional[Callable] = None,
    ):
        def _worker():
            start_res = self.start_emergency_session()
            if start_res.get("ok") and lat is not None and lon is not None:
                sid = start_res.get("data", {}).get("session_id")
                if sid:
                    self.update_emergency_location(sid, lat, lon, accuracy)
            if callback:
                callback(start_res)
        threading.Thread(target=_worker, daemon=True).start()

    def async_complete_emergency(self, session_id: str, callback: Optional[Callable] = None):
        def _worker():
            res = self.complete_emergency_session(session_id)
            if callback:
                callback(res)
        threading.Thread(target=_worker, daemon=True).start()
