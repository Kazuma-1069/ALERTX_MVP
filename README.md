# ALERTX MVP

Simple personal safety Android MVP based on the supplied Stitch "Guardian Modern" design.

## MVP flow

1. Open ALERTX.
2. Save one trusted emergency contact.
3. Press and hold SOS for 2 seconds.
4. Get the current location.
5. Send an emergency SMS containing a Google Maps link.
6. Show emergency status and allow cancellation.

## Stack

- Kivy + KivyMD
- Plyer for device location where supported
- Pyjnius for native Android SMS integration
- FastAPI + SQLAlchemy + SQLite
- httpx
- pytest
- Buildozer

## Run the backend

```bash
python -m venv .venv
# Windows CMD:
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Run the UI on desktop

Install Kivy/KivyMD, then:

```bash
python app/main.py
```

Native GPS/SMS behavior requires an Android build.

## Android build

From a Linux/macOS environment or WSL with Buildozer:

```bash
cd app
buildozer android debug
```

## Important MVP limitation

SMS and GPS are device/permission dependent. On desktop, the app uses safe demo/fallback behavior so the UI can be developed without Android hardware.
