# Stitch → Kivy/KivyMD mapping

The supplied Stitch export is the visual source of truth.

## Home

Stitch: `alertx_home_screen/code.html`

Converted into:
- `app/screens/home.py`
- Home screen KV in `app/main.py`

Preserved concepts:
- ALERTX header
- shield branding
- online status
- emergency contact card
- large SOS action
- clear hold-to-prevent-false-alarms messaging
- bottom navigation actions

## Emergency Contacts

Stitch: `alertx_emergency_contact/code.html`

Converted into:
- `app/screens/contacts.py`

Preserved concepts:
- Lifeline Guardian heading
- one trusted primary contact
- name
- relationship
- phone
- save contact
- verification/status feedback

## Emergency Active

Stitch: `alertx_emergency_active/code.html`

Converted into:
- `app/screens/emergency.py`

Preserved concepts:
- Active SOS Dispatch
- Emergency Active state
- session ID
- location status
- coordinates
- SMS status
- recipient
- cancellation action

## Design system

Based on supplied `guardian_modern/DESIGN.md`:
- Inter typography direction
- light blue/white surfaces
- cobalt blue primary interaction
- crimson red emergency state
- rounded cards
- high-contrast emergency messaging
- large touch targets
