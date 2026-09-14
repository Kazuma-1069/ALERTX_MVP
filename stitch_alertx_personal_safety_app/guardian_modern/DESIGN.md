---
name: Guardian Modern
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#45464d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#0051d5'
  on-secondary: '#ffffff'
  secondary-container: '#316bf3'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#410002'
  on-tertiary-container: '#f63a35'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#dbe1ff'
  secondary-fixed-dim: '#b4c5ff'
  on-secondary-fixed: '#00174b'
  on-secondary-fixed-variant: '#003ea8'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#93000b'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: '800'
    lineHeight: 64px
    letterSpacing: -0.02em
  display-sm:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.05em
  emergency-counter:
    fontFamily: Inter
    fontSize: 72px
    fontWeight: '900'
    lineHeight: 72px
    letterSpacing: -0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-sm: 0.75rem
  margin: 1.25rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system serves high-stress emergency, personal protection, and critical alert scenarios on Android devices. It synthesizes the utilitarian clarity of modern Android (Material 3) with an ultra-accessible, life-safety user interface.

### Brand Personality & Emotional Core
- **Unflappable Calm:** In regular usage (setup, safety checks, contact updates, trip monitoring), the interface is serene, quiet, and dependable, minimizing cognitive friction and anxiety.
- **Immediate Urgency & Absolute Clarity:** In active crisis or SOS dispatch, the interface transforms decisively into an authoritative, fail-safe visual state with maximum contrast and unmissable affordances.
- **Physical Defensiveness:** Designed explicitly for extreme physical conditions—trembling hands, low visibility, glare, split-second reflexes, and one-handed operation.

### Visual Aesthetic
- **Modern Material Adaptive:** Anchored in clean surfaces, systematic paddings, and deliberate tonal hierarchy, strictly respecting Android system bars, gesture insets, and standard top/bottom navigation mechanics.
- **Zero Ambiguity:** Eliminates decorative artifacts, low-contrast subtle iconography, or complex gesture requirements in favour of oversized touch targets, tactile button confirmations, and clear status badges.

## Colors

The color architecture is built upon a two-state operational paradigm: **Resting/Monitoring State** and **Emergency/SOS State**, supplemented by standard status feedback.

### Nominal & Surveillance State
- **Surface Base:** `#F8FAFC` (Slate 50) creates an anti-glare canvas that preserves battery and visual comfort.
- **Surface Container:** `#FFFFFF` (Pure White) defines interactive cards, sheets, and elevated modules.
- **Primary Text & Structure:** `#0F172A` (Deep Slate 900) ensures a contrast ratio exceeding 14:1 on white surfaces.
- **Secondary Structural:** `#334155` (Slate 700) for subheaders, supporting text, and secondary toolbars.
- **Subtle Outline:** `#E2E8F0` (Slate 200) provides structural bounds without introducing visual noise.
- **Muted Content & Icons:** `#64748B` (Slate 500) strictly for non-critical metadata and inactive states.
- **Accent / Interactive:** `#2563EB` (Cobalt Blue 600) for regular action items, primary navigation triggers, and link elements.

### Emergency & Crisis State
When SOS triggers or active danger is sensed, the viewport adopts the emergency tonal set:
- **Emergency Dominant:** `#DC2626` (Crimson Red 600) for high-impact action surfaces, countdown banners, and the primary SOS dispatch trigger.
- **Emergency Dark:** `#991B1B` (Deep Crimson 800) for high-stress contrast borders, active trigger press states, and urgent critical headers.
- **Emergency Light Surface:** `#FEF2F2` (Crimson 50) for background containment of active incident details and audio recording trackers.
- **Emergency Surface Outline:** `#FECACA` (Crimson 200) for structural division in crisis mode.
- **Emergency Foreground:** `#FFFFFF` for absolute legibility over primary red tokens (contrast ratio > 4.5:1).

### Status Indicators
- **Safe / Active Guardian / Verified:** `#059669` (Emerald 600), paired with `#ECFDF5` background.
- **Caution / Battery Depletion / Poor Signal:** `#D97706` (Amber 600), paired with `#FFFBEB` background.

## Typography

Typography prioritizes rapid cognitive absorption under acute psychological stress. Inter provides uniform geometric proportions, clear numerals, and unambiguous character forms (e.g., distinguishing uppercase `I`, lowercase `l`, and the number `1`).

### Hierarchy & Scale Guidelines
- **Emergency Counter (`emergency-counter`):** Reserved solely for time-critical cancellation counters (e.g., "Dispatching in 5... 4... 3...") and live dispatch clocks.
- **Display Scales (`display-lg`, `display-sm`):** Primary SOS prompts and mission-critical status announcements ("SOS TRANSMITTED", "CRASH DETECTED").
- **Headlines:** Clear, short, front-loaded phrasing. Sentences must be concise and directive.
- **Body:** Generous line-height (`1.5`) guarantees line isolation when a user is walking briskly or experiencing hand tremors.
- **Labels:** Semibold and bold weights ensure button commands and touch interactive items are scannable in peripheral vision.

## Layout & Spacing

The layout is grounded in a mobile-first, strict 4-column Android grid designed around thumb-reach zones and Android system gesture safe insets.

### Reachability Architecture (Thumb-Zone Priority)
- **Primary Interactive Region:** Placed strictly within the bottom 60% of the screen. Critical emergency buttons, quick-dial contacts, and the SOS trigger reside in the bottom third.
- **Status & Passive Telemetry Region:** Top 40% of the screen houses passive verification indicators (GPS precision, battery health, cellular connection strength).

### Grid & Breakpoints
- **Compact (Android Phone Portrait, < 600dp):** 4-column fluid layout with `16px` (1rem) gutters and `20px` (1.25rem) side margins.
- **Expanded / Foldable Unfolded (>= 600dp):** 8-column layout with `24px` gutters and `32px` margins; emergency action panels dock to the dominant hand side with secondary telemetry split into a companion panel.

### Spatial Rhythm
All spacing adheres strictly to an 8px cadence (with 4px for micro-alignments):
- Component internal padding uses `space-md` (16px) or `space-lg` (24px).
- Vertical stack flow between unrelated cards enforces `space-lg` (24px) to avoid accidental taps.
- Touch target minimum spacing enforces at least `space-sm` (8px) between any adjacent interactive surfaces.

## Elevation & Depth

Depth is established via modern Material You tonal stacking combined with ultra-soft, diffused ambient shadows. In high-stress mobile contexts, stark multi-layered 3D skeuomorphism distracts from information hierarchy; clean tonal tiering keeps cognitive focus on active tasks.

### Elevation Levels

- **Level 0 (Canvas Base):** Surface base `#F8FAFC`. Unbacked, passive screen ground.
- **Level 1 (Card & Content Surface):** Surface Container `#FFFFFF` with a 1px structural stroke (`#E2E8F0`). Flat or supported by an ambient drop shadow:
  - `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`
- **Level 2 (Interactive Floating Modules & Sticky Bars):** Bottom action sheets, pinned safety monitors, and secondary FABs:
  - `0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05)`
- **Level 3 (Modal Alerts & Active Emergency Overlays):** Full-screen emergency dispatches, cancellation sliders, and system interrupt dialogs:
  - `0 20px 25px -5px rgba(15, 23, 42, 0.12), 0 8px 10px -6px rgba(15, 23, 42, 0.08)`
- **Emergency SOS Aura (Active Crisis Mode):** The main SOS button utilizes a dynamic, pulsating diffused crimson shadow to telegraph activation readiness:
  - `0 0 0 8px rgba(220, 38, 38, 0.2), 0 12px 24px -4px rgba(220, 38, 38, 0.4)`

## Shapes

The shape system employs soft, organic roundedness reflecting current Android visual design, instilling safety, physical comfort, and modern software polish.

### Geometry Specifications
- **Standard Structural Cards:** `16px` (`rounded-lg` token mapping) creates friendly, easily segmented units of information without consuming excessive screen real estate.
- **Large Content Surfaces & Bottom Sheets:** `24px` to `28px` (`rounded-xl` token mapping) for modal sheets and top safety status banners, matching Android 14/15 bottom sheet standard radiuses.
- **Interactive Buttons & Chips:** 
  - Standard action buttons utilize `16px` radiuses.
  - Quick action status chips and pill controls use fully rounded pill geometry (`9999px`).
  - **The Central SOS Trigger:** Fully circular (`rounded-full`), sized at a massive minimum of `120px × 120px` to `160px × 160px` to guarantee physical accessibility regardless of how the device is held.

## Components

### Buttons & SOS Triggers
- **Emergency SOS Button:** Circular container (`140px` diameter minimum), background `#DC2626`, active ripple `#991B1B`. Features centered bold label (`label-lg`, `#FFFFFF`) plus universal safety icon. Requires a 2-second continuous press or slide-confirmation to prevent accidental pocket triggers. Surrounded by an animated ring buffer during holding.
- **Primary Nominal Action Buttons:** Minimum height of `56px` to comply with extreme-stress motor control benchmarks. Filled with `#0F172A` text `#FFFFFF`, corner radius `16px`, full width on mobile canvas.
- **Secondary Buttons:** Minimum height `56px`, 1.5px border `#E2E8F0`, background `#FFFFFF`, text `#0F172A`.
- **Cancel SOS Slider:** Horizontal drag component, minimum `64px` height, `#FEF2F2` background, with a prominent `#DC2626` thumb require full rightward track completion to abort an alert.

### Status Badges & Chips
- **System Monitoring Chips:** `36px` height, fully pill-shaped. Composed of a `8px` pulsating status dot (e.g., `#059669` for "GPS High Accuracy"), followed by `label-md` text. Background uses corresponding tonal wash (e.g., `#ECFDF5`).
- **Emergency Contact Quick-Chips:** `48px` minimum height, allowing direct single-tap voice or location broadcast during a pre-alarm state.

### Cards & Telemetry Lists
- **Safety Card:** White surface, `16px` border radius, `1px` subtle stroke `#E2E8F0`. Padding `space-lg` (24px). Contains prominent left-aligned headline, icon indicator, and clear action button.
- **List Items (Emergency Contacts, Check-in logs):** Minimum row height of `72px` with integrated large touch regions (minimum `48px × 48px` action icons for calling or reordering contacts).

### Inputs & Verification Form Fields
- **Emergency Medical & Identity Fields:** `56px` container height, rounded `12px` border, `#F8FAFC` background resting state, transitioning to `#2563EB` 2px border on focus. Label text remains visible above field at all times (`label-sm`).

### Android Native Shell Accommodations
- **Top App Bar:** Left-aligned, non-collapsing title (`headline-md`), clean back arrow navigation (`48px` touch target), integrated cellular/satellite readiness glyph.
- **Bottom System Navigation:** Clean 3 or 4 item bar, height `80px` inclusive of system gesture area, active indicator utilizing soft capsule background indicator (`#E2E8F0`).