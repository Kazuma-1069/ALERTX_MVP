"""AlertX Location Service.

Integrates real GPS positioning via Plyer / Android Location Providers.
Extracts latitude, longitude, accuracy, and timestamp, and generates
Google Maps location links for emergency alerts.
Never fabricates fake coordinates.
"""

import time
from typing import Any, Dict, Optional


class LocationService:
    """Service to monitor and retrieve real GPS location."""

    def __init__(self):
        self._latest_fix: Optional[Dict[str, Any]] = None
        self._is_active = False
        self._start_gps_listener()

    def _start_gps_listener(self):
        """Configure and start background GPS listening."""
        try:
            from plyer import gps

            def _on_location(**kwargs):
                lat = kwargs.get("lat")
                lon = kwargs.get("lon")
                if lat is not None and lon is not None:
                    self._latest_fix = {
                        "lat": float(lat),
                        "lon": float(lon),
                        "accuracy": float(kwargs.get("accuracy", 0.0) or 0.0),
                        "altitude": kwargs.get("altitude"),
                        "timestamp": time.time(),
                    }

            def _on_status(stype, status):
                pass

            gps.configure(on_location=_on_location, on_status=_on_status)
            gps.start(minTime=1000, minDistance=1)
            self._is_active = True
        except Exception:
            # GPS hardware or Plyer unavailable on this platform
            self._is_active = False

    def get_current(self) -> Dict[str, Any]:
        """Retrieve the current real GPS position.

        Returns a dictionary with status and coordinates. If no real fix is
        available, explicitly reports 'Unable to obtain current location'
        without faking.
        """
        if self._latest_fix and self._latest_fix.get("lat") is not None:
            lat = self._latest_fix["lat"]
            lon = self._latest_fix["lon"]
            accuracy = self._latest_fix.get("accuracy", 0.0)
            maps_url = self.generate_maps_url(lat, lon)
            coords_str = self.format_coordinates(lat, lon)

            return {
                "ok": True,
                "status": "High Precision" if accuracy <= 10 else "GPS Acquired",
                "lat": lat,
                "lon": lon,
                "accuracy": accuracy,
                "accuracy_str": f"Within ±{accuracy:.1f} meters" if accuracy else "GPS Lock",
                "coordinates_str": coords_str,
                "maps_url": maps_url,
                "timestamp": self._latest_fix.get("timestamp", time.time()),
            }

        return {
            "ok": False,
            "status": "Unavailable",
            "lat": None,
            "lon": None,
            "accuracy": None,
            "accuracy_str": "No satellite lock",
            "coordinates_str": "Unable to obtain current location",
            "maps_url": None,
            "message": "Unable to obtain current location.",
            "timestamp": time.time(),
        }

    @staticmethod
    def generate_maps_url(lat: float, lon: float) -> str:
        """Generate standard Google Maps location URL."""
        return f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"

    @staticmethod
    def format_coordinates(lat: float, lon: float) -> str:
        """Format coordinates into clean readable string (e.g. 37.7749° N, 122.4194° W)."""
        lat_dir = "N" if lat >= 0 else "S"
        lon_dir = "E" if lon >= 0 else "W"
        return f"{abs(lat):.4f}° {lat_dir}, {abs(lon):.4f}° {lon_dir}"

    def set_mock_location_for_testing(self, lat: float, lon: float, accuracy: float = 3.2):
        """Explicit mock injector intended solely for automated unit testing."""
        self._latest_fix = {
            "lat": lat,
            "lon": lon,
            "accuracy": accuracy,
            "timestamp": time.time(),
        }
