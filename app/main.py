import sys
from pathlib import Path

# Ensure app directory is on path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

from services.emergency import EmergencyService
from services.location import LocationService
from services.sms import SmsService
from services.calling import CallingService
from utils.constants import APP_NAME

from screens.home import HomeScreen
from screens.contacts import ContactsScreen
from screens.emergency import EmergencyScreen
from screens.settings import SettingsScreen


class ClickableCard(MDCard):
    """Card with click behavior and subtle touch response."""
    pass


KV = '''#:import dp kivy.metrics.dp

<ClickableCard>:
    ripple_behavior: True

<MDIcon>:
    size_hint: None, None
    size: self.font_size, self.font_size

<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"
        theme_bg_color: "Custom"
        md_bg_color: app.bg_surface

        # TOP APP HEADER
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            padding: dp(16), dp(10)
            spacing: dp(12)
            theme_bg_color: "Custom"
            md_bg_color: app.bg_surface

            MDCard:
                size_hint: None, None
                size: dp(42), dp(42)
                radius: [12, 12, 12, 12]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.blue
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=12sp][color=38BDF8]ALERTX[/color][/size]   [color=64748B]•[/color]   [size=16sp][color=F8FAFC]Home[/color][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            # Online capsule badge
            MDCard:
                size_hint: None, None
                size: dp(118), dp(30)
                radius: [self.height / 2, self.height / 2, self.height / 2, self.height / 2]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                padding: dp(10), dp(4)
                spacing: dp(6)
                pos_hint: {"center_y": .5}

                MDCard:
                    size_hint: None, None
                    size: dp(8), dp(8)
                    radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                    pos_hint: {"center_y": .5}
                    theme_bg_color: "Custom"
                    md_bg_color: app.green if root.online_badge_text == "ONLINE" else app.blue

                MDLabel:
                    text: root.online_badge_text
                    font_size: "11sp"
                    bold: True
                    adaptive_size: True
                    theme_text_color: "Custom"
                    text_color: app.green if root.online_badge_text == "ONLINE" else app.blue
                    pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(36), dp(36)
                radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "20sp"

        # SCROLLABLE CONTENT
        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(16), dp(16), dp(84)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # ALERTX PRO / ARMED BANNER
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(54)
                    spacing: dp(12)

                    MDCard:
                        size_hint: None, None
                        size: dp(46), dp(46)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_lowest
                        line_color: app.surface_container
                        line_width: 1
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "shield-plus"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.crimson_coral
                            font_size: "26sp"

                    MDLabel:
                        markup: True
                        text: root.banner_markup
                        pos_hint: {"center_y": .5}

                    Widget:

                    # Armed Badge
                    MDCard:
                        size_hint: None, None
                        size: dp(106), dp(32)
                        radius: [16, 16, 16, 16]
                        theme_bg_color: "Custom"
                        md_bg_color: app.green_light
                        line_color: app.green
                        line_width: 1
                        padding: dp(8), dp(4)
                        spacing: dp(6)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "shield-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "ARMED"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.green
                            pos_hint: {"center_y": .5}

                # CARD 1: EMERGENCY CONTACT
                ClickableCard:
                    orientation: "horizontal"
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(82)
                    on_release: app.go_contacts()

                    MDCard:
                        size_hint: None, None
                        size: dp(44), dp(44)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "card-account-phone"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "24sp"

                    MDLabel:
                        markup: True
                        text: root.contact_markup
                        pos_hint: {"center_y": .5}

                    MDCard:
                        size_hint: None, None
                        size: dp(96), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: app.green_light
                        padding: dp(8), dp(2)
                        spacing: dp(4)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "check-circle"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: root.contact_badge
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.green
                            pos_hint: {"center_y": .5}

                # CARD 2: LOCATION SERVICES
                MDCard:
                    orientation: "horizontal"
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(82)

                    MDCard:
                        size_hint: None, None
                        size: dp(44), dp(44)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "map-marker-radius"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "24sp"

                    MDLabel:
                        markup: True
                        text: root.location_markup
                        pos_hint: {"center_y": .5}

                    MDCard:
                        size_hint: None, None
                        size: dp(76), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0.05, 0.29, 0.43, 0.4]
                        padding: dp(8), dp(2)
                        spacing: dp(4)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "satellite-uplink"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "Live"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.blue
                            pos_hint: {"center_y": .5}

                # CENTRAL SOS BUTTON SECTION
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(350)
                    padding: dp(0), dp(4)
                    spacing: dp(14)

                    # Concentric Glowing Rings & Central SOS Beacon
                    AnchorLayout:
                        anchor_x: "center"
                        anchor_y: "center"
                        size_hint_y: None
                        height: dp(246)

                        # Outer Soft Aura (Glow Ring 1)
                        MDCard:
                            size_hint: None, None
                            size: dp(240), dp(240)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            theme_bg_color: "Custom"
                            md_bg_color: [0.93, 0.26, 0.26, 0.10]

                        # Inner Aura (Glow Ring 2)
                        MDCard:
                            size_hint: None, None
                            size: dp(204), dp(204)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            theme_bg_color: "Custom"
                            md_bg_color: [0.93, 0.26, 0.26, 0.22]

                        # Main Crimson SOS Button
                        ClickableCard:
                            size_hint: None, None
                            size: dp(174), dp(174)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            elevation: 6
                            theme_bg_color: "Custom"
                            md_bg_color: app.crimson
                            on_touch_down: if self.collide_point(*args[1].pos): root.on_sos_press()
                            on_touch_up: root.on_sos_release()

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(12), dp(10)
                                spacing: dp(2)
                                pos_hint: {"center_x": .5, "center_y": .5}

                                AnchorLayout:
                                    anchor_x: "center"
                                    anchor_y: "center"
                                    size_hint_y: None
                                    height: dp(42)

                                    MDCard:
                                        size_hint: None, None
                                        size: dp(42), dp(42)
                                        radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                                        theme_bg_color: "Custom"
                                        md_bg_color: [1, 1, 1, 0.22]

                                        AnchorLayout:
                                            anchor_x: "center"
                                            anchor_y: "center"

                                            MDIcon:
                                                icon: "power"
                                                theme_text_color: "Custom"
                                                text_color: app.white
                                                font_size: "24sp"

                                MDLabel:
                                    text: "SOS"
                                    font_size: "36sp"
                                    bold: True
                                    halign: "center"
                                    valign: "middle"
                                    theme_text_color: "Custom"
                                    text_color: app.white
                                    size_hint_y: None
                                    height: dp(42)

                                MDLabel:
                                    text: "EMERGENCY"
                                    font_size: "10sp"
                                    bold: True
                                    halign: "center"
                                    valign: "middle"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.85]
                                    size_hint_y: None
                                    height: dp(16)

                    # Info Badge below button
                    MDCard:
                        size_hint: None, None
                        size: dp(260), dp(32)
                        radius: [self.height / 2, self.height / 2, self.height / 2, self.height / 2]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_lowest
                        line_color: app.surface_container
                        line_width: 1
                        padding: dp(12), dp(4)
                        spacing: dp(6)
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "gesture-tap-hold"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "16sp"
                            size_hint_x: None
                            width: dp(16)
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: root.sos_status_text
                            font_size: "11sp"
                            bold: True
                            adaptive_size: True
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            pos_hint: {"center_y": .5}

                    MDLabel:
                        text: "Press & hold to initiate emergency alert"
                        font_size: "13sp"
                        bold: True
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_primary
                        size_hint_y: None
                        height: dp(20)

                    MDLabel:
                        text: "Sends instant SMS with GPS coordinates to your contact"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary
                        size_hint_y: None
                        height: dp(18)

                # CARD 3: SYSTEM DEFENSE READY
                MDCard:
                    orientation: "horizontal"
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 0
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(100)

                    MDCard:
                        size_hint: None, None
                        size: dp(40), dp(40)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "shield-check"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "24sp"

                    MDLabel:
                        markup: True
                        text: root.defense_summary_markup
                        font_size: "13sp"
                        pos_hint: {"center_y": .5}

        # BOTTOM NAVIGATION BAR
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            theme_bg_color: "Custom"
            md_bg_color: app.surface_lowest
            padding: dp(8), dp(4)

            # Home Tab (Active)
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_home()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_container
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"

                    MDLabel:
                        text: "Home"
                        font_size: "11sp"
                        bold: True
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_primary

            # Contacts Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_contacts()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "card-account-phone"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Contacts"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            # Safety Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_safety()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield-check"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Safety"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            # Help Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_help()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "information-outline"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Help"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary


<ContactsScreen>:
    name: "contacts"

    MDBoxLayout:
        orientation: "vertical"
        theme_bg_color: "Custom"
        md_bg_color: app.bg_surface

        # TOP APP HEADER
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            padding: dp(16), dp(10)
            spacing: dp(12)
            theme_bg_color: "Custom"
            md_bg_color: app.bg_surface

            MDCard:
                size_hint: None, None
                size: dp(42), dp(42)
                radius: [12, 12, 12, 12]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.blue
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=12sp][color=38BDF8]ALERTX[/color][/size]   [color=64748B]•[/color]   [size=16sp][color=F8FAFC]Emergency Contacts[/color][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(96), dp(30)
                radius: [15, 15, 15, 15]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                padding: dp(8), dp(4)
                spacing: dp(6)
                pos_hint: {"center_y": .5}

                MDCard:
                    size_hint: None, None
                    size: dp(8), dp(8)
                    radius: [4, 4, 4, 4]
                    pos_hint: {"center_y": .5}
                    theme_bg_color: "Custom"
                    md_bg_color: app.green

                MDLabel:
                    text: "ONLINE"
                    font_size: "11sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app.green
                    pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(36), dp(36)
                radius: [18, 18, 18, 18]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "20sp"

        # SCROLLABLE CONTENT
        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(8), dp(16), dp(84)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # SCREEN INTRO
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(72)
                    spacing: dp(4)

                    MDBoxLayout:
                        spacing: dp(4)
                        size_hint_y: None
                        height: dp(18)

                        MDIcon:
                            icon: "shield-check"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "LIFELINE GUARDIAN"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.blue
                            pos_hint: {"center_y": .5}

                    MDLabel:
                        markup: True
                        text: root.intro_markup
                        size_hint_y: None
                        height: dp(48)

                # AUTOMATED SOS PROTOCOL INFO CARD
                MDCard:
                    orientation: "horizontal"
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 0
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(94)

                    MDCard:
                        size_hint: None, None
                        size: dp(42), dp(42)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "email-fast-outline"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "22sp"

                    MDLabel:
                        markup: True
                        text: root.automated_sos_markup
                        font_size: "13sp"
                        pos_hint: {"center_y": .5}

                # ACTIVE GUARDIAN CARD
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(6)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(24)

                        MDLabel:
                            text: "ACTIVE GUARDIAN"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.text_secondary

                        Widget:

                        MDCard:
                            size_hint: None, None
                            size: dp(86), dp(24)
                            radius: [12, 12, 12, 12]
                            theme_bg_color: "Custom"
                            md_bg_color: app.green_light
                            line_color: app.green
                            line_width: 1
                            padding: dp(8), dp(2)
                            spacing: dp(4)

                            MDCard:
                                size_hint: None, None
                                size: dp(6), dp(6)
                                radius: [3, 3, 3, 3]
                                pos_hint: {"center_y": .5}
                                theme_bg_color: "Custom"
                                md_bg_color: app.green

                            MDLabel:
                                text: "Primary"
                                font_size: "11sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.green

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(14)
                        radius: [16, 16, 16, 16]
                        elevation: 1
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_lowest
                        line_color: app.surface_container
                        line_width: 1
                        size_hint_y: None
                        height: dp(136)

                        MDBoxLayout:
                            spacing: dp(12)
                            size_hint_y: None
                            height: dp(48)

                            MDCard:
                                size_hint: None, None
                                size: dp(48), dp(48)
                                radius: [24, 24, 24, 24]
                                theme_bg_color: "Custom"
                                md_bg_color: app.surface_low
                                line_color: app.blue
                                line_width: 1
                                pos_hint: {"center_y": .5}

                                MDLabel:
                                    text: root.guardian_initials
                                    font_size: "18sp"
                                    bold: True
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: app.blue

                            MDBoxLayout:
                                orientation: "vertical"
                                pos_hint: {"center_y": .5}

                                MDBoxLayout:
                                    spacing: dp(6)
                                    size_hint_y: None
                                    height: dp(22)

                                    MDLabel:
                                        text: root.guardian_name
                                        font_size: "17sp"
                                        bold: True
                                        theme_text_color: "Custom"
                                        text_color: app.text_primary

                                    MDCard:
                                        size_hint: None, None
                                        size: dp(72), dp(22)
                                        radius: [6, 6, 6, 6]
                                        theme_bg_color: "Custom"
                                        md_bg_color: app.surface_low
                                        padding: dp(6), dp(2)

                                        MDLabel:
                                            text: root.guardian_relation
                                            font_size: "11sp"
                                            halign: "center"
                                            theme_text_color: "Custom"
                                            text_color: app.text_secondary

                                MDLabel:
                                    text: root.guardian_phone
                                    font_size: "13sp"
                                    theme_text_color: "Custom"
                                    text_color: app.text_secondary

                        MDBoxLayout:
                            size_hint_y: None
                            height: dp(34)
                            spacing: dp(8)

                            MDBoxLayout:
                                spacing: dp(4)
                                pos_hint: {"center_y": .5}

                                MDIcon:
                                    icon: "check-circle"
                                    theme_text_color: "Custom"
                                    text_color: app.green
                                    font_size: "18sp"

                                MDLabel:
                                    text: "Verified for SMS alerts"
                                    font_size: "12sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.green

                            ClickableCard:
                                size_hint: None, None
                                size: dp(120), dp(32)
                                radius: [16, 16, 16, 16]
                                theme_bg_color: "Custom"
                                md_bg_color: app.surface_low
                                line_color: app.surface_container
                                line_width: 1
                                padding: dp(8), dp(4)
                                spacing: dp(4)
                                on_release: root.test_alert()

                                MDIcon:
                                    icon: "message-text"
                                    theme_text_color: "Custom"
                                    text_color: app.blue
                                    font_size: "16sp"
                                    pos_hint: {"center_y": .5}

                                MDLabel:
                                    text: "Test Alert"
                                    font_size: "11sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.text_primary
                                    pos_hint: {"center_y": .5}

                # UPDATE CONTACT DETAILS FORM
                MDCard:
                    orientation: "vertical"
                    padding: dp(18)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(336)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(24)

                        MDLabel:
                            text: "Update Contact Details"
                            font_size: "16sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.text_primary

                        MDIcon:
                            icon: "square-edit-outline"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    # Field 1: Full Name
                    MDLabel:
                        text: "FULL NAME"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.text_secondary
                        size_hint_y: None
                        height: dp(14)

                    MDCard:
                        size_hint_y: None
                        height: dp(48)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        padding: dp(12), dp(4)
                        spacing: dp(8)

                        MDIcon:
                            icon: "account-details"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}

                        TextInput:
                            id: name_field
                            text: "Sarah Jenkins"
                            hint_text: "Full Name"
                            cursor_color: app.blue
                            background_color: [0, 0, 0, 0]
                            foreground_color: [0.97, 0.98, 0.99, 1]
                            hint_text_color: [0.39, 0.45, 0.54, 1]
                            font_size: "15sp"
                            multiline: False
                            pos_hint: {"center_y": .5}

                    # Field 2: Relationship Selector Pills
                    MDLabel:
                        text: "RELATIONSHIP (OPTIONAL)"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.text_secondary
                        size_hint_y: None
                        height: dp(14)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(8)

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.blue if root.selected_relation == "Parent" else app.surface_low
                            on_release: root.select_relation("Parent")

                            MDLabel:
                                text: "Parent"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.black if root.selected_relation == "Parent" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.blue if root.selected_relation == "Spouse" else app.surface_low
                            on_release: root.select_relation("Spouse")

                            MDLabel:
                                text: "Spouse"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.black if root.selected_relation == "Spouse" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.blue if root.selected_relation == "Sibling" else app.surface_low
                            on_release: root.select_relation("Sibling")

                            MDLabel:
                                text: "Sibling"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.black if root.selected_relation == "Sibling" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.blue if root.selected_relation == "Friend" else app.surface_low
                            on_release: root.select_relation("Friend")

                            MDLabel:
                                text: "Friend"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.black if root.selected_relation == "Friend" else app.text_secondary

                    # Field 3: Phone Number
                    MDLabel:
                        text: "PHONE NUMBER"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.text_secondary
                        size_hint_y: None
                        height: dp(14)

                    MDCard:
                        size_hint_y: None
                        height: dp(48)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        padding: dp(12), dp(4)
                        spacing: dp(6)

                        MDIcon:
                            icon: "cellphone"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "US +1"
                            font_size: "13sp"
                            bold: True
                            size_hint_x: None
                            width: dp(44)
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            pos_hint: {"center_y": .5}

                        TextInput:
                            id: phone_field
                            text: "(555) 234-5678"
                            hint_text: "Phone Number"
                            input_type: "tel"
                            cursor_color: app.blue
                            background_color: [0, 0, 0, 0]
                            foreground_color: [0.97, 0.98, 0.99, 1]
                            hint_text_color: [0.39, 0.45, 0.54, 1]
                            font_size: "15sp"
                            multiline: False
                            pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "check-circle"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}

                    # Save Contact Button
                    ClickableCard:
                        size_hint_y: None
                        height: dp(50)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.blue
                        padding: dp(12), dp(4)
                        spacing: dp(8)
                        on_release: root.save_contact()

                        MDBoxLayout:
                            spacing: dp(8)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            MDIcon:
                                icon: "content-save"
                                theme_text_color: "Custom"
                                text_color: app.black
                                font_size: "20sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Save Contact"
                                font_size: "15sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.black
                                pos_hint: {"center_y": .5}

                # CONTACT PERMISSIONS CARD
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 0
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(138)

                    MDLabel:
                        text: "CONTACT PERMISSIONS"
                        font_size: "11sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.text_secondary
                        size_hint_y: None
                        height: dp(16)

                    MDBoxLayout:
                        spacing: dp(12)
                        size_hint_y: None
                        height: dp(40)

                        MDCard:
                            size_hint: None, None
                            size: dp(36), dp(36)
                            radius: [18, 18, 18, 18]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "map-marker-radius"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "18sp"

                        MDBoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Live Pin Tracking"
                                font_size: "14sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.text_primary

                            MDLabel:
                                text: "Sends dynamic map pin refreshed with precision"
                                font_size: "11sp"
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                    MDBoxLayout:
                        spacing: dp(12)
                        size_hint_y: None
                        height: dp(40)

                        MDCard:
                            size_hint: None, None
                            size: dp(36), dp(36)
                            radius: [18, 18, 18, 18]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "transmission-tower"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "18sp"

                        MDBoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Cellular Bypass"
                                font_size: "14sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.text_primary

                            MDLabel:
                                text: "Prioritizes delivery through emergency carrier band"
                                font_size: "11sp"
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                # TOAST / FEEDBACK MESSAGE
                MDLabel:
                    text: root.status_toast
                    font_size: "13sp"
                    bold: True
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.green
                    size_hint_y: None
                    height: dp(24) if root.status_toast else dp(0)

        # BOTTOM NAVIGATION BAR (Contacts Active)
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            theme_bg_color: "Custom"
            md_bg_color: app.surface_lowest
            padding: dp(8), dp(4)

            # Home Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_home()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Home"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            # Contacts Tab (Active)
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_contacts()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_container
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "card-account-phone"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"

                    MDLabel:
                        text: "Contacts"
                        font_size: "11sp"
                        bold: True
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_primary

            # Safety Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_safety()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield-check"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Safety"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            # Help Tab
            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_help()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "information-outline"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Help"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary


<SettingsScreen>:
    name: "safety"

    MDBoxLayout:
        orientation: "vertical"
        theme_bg_color: "Custom"
        md_bg_color: app.bg_surface

        # TOP APP HEADER
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            padding: dp(16), dp(10)
            spacing: dp(12)
            theme_bg_color: "Custom"
            md_bg_color: app.bg_surface

            MDCard:
                size_hint: None, None
                size: dp(42), dp(42)
                radius: [12, 12, 12, 12]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.blue
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=12sp][color=38BDF8]ALERTX[/color][/size]   [color=64748B]•[/color]   [size=16sp][color=F8FAFC]Safety & SOS Settings[/color][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(36), dp(36)
                radius: [18, 18, 18, 18]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "20sp"

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(10), dp(16), dp(84)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(236)

                    MDLabel:
                        text: "EMERGENCY SOS MESSAGE TEMPLATE"
                        font_size: "11sp"
                        bold: True
                        size_hint_y: None
                        height: dp(18)
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

                    MDCard:
                        padding: dp(12)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        size_hint_y: None
                        height: dp(112)

                        MDLabel:
                            text: root.message_preview
                            font_size: "12sp"
                            italic: True
                            theme_text_color: "Custom"
                            text_color: app.text_primary

                    ClickableCard:
                        size_hint_y: None
                        height: dp(40)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        line_color: app.surface_container
                        line_width: 1
                        on_release: root.reset_template()

                        MDLabel:
                            text: "Restore Default SOS Template"
                            font_size: "12sp"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: app.blue

                # SYSTEM & HARDWARE DIAGNOSTICS CARD
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(290)

                    MDLabel:
                        text: "SYSTEM & HARDWARE STATUS"
                        font_size: "11sp"
                        bold: True
                        size_hint_y: None
                        height: dp(18)
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(26)
                        MDIcon:
                            icon: "crosshairs-gps"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: root.gps_status_text
                            font_size: "12sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(26)
                        MDIcon:
                            icon: "message-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: root.sms_status_text
                            font_size: "12sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(26)
                        MDIcon:
                            icon: "phone-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: root.call_status_text
                            font_size: "12sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(34)
                        MDIcon:
                            icon: "cloud-sync"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: root.cloud_status_text
                            font_size: "12sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    ClickableCard:
                        size_hint_y: None
                        height: dp(38)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        line_color: app.surface_container
                        line_width: 1
                        on_release: root.request_all_permissions()

                        MDBoxLayout:
                            spacing: dp(6)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            MDIcon:
                                icon: "shield-lock-outline"
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "18sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Verify & Request System Permissions"
                                font_size: "12sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.blue
                                pos_hint: {"center_y": .5}

                # EMERGENCY SOS PROTOCOL & HELP CARD
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(210)

                    MDLabel:
                        text: "EMERGENCY PROTOCOL & HELP GUIDE"
                        font_size: "11sp"
                        bold: True
                        size_hint_y: None
                        height: dp(18)
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(36)
                        MDIcon:
                            icon: "gesture-tap-hold"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Press & hold SOS for 2 seconds to initiate emergency broadcast."
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(36)
                        MDIcon:
                            icon: "satellite-uplink"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Satellite GPS & SMS operate without Internet data or Wi-Fi."
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(8)
                        size_hint_y: None
                        height: dp(36)
                        MDIcon:
                            icon: "shield-refresh"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Press and hold Cancel on the Active screen to resolve an alert."
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                # APP VERSION & BUILD CARD
                MDCard:
                    orientation: "vertical"
                    padding: dp(14), dp(10)
                    spacing: dp(4)
                    radius: [14, 14, 14, 14]
                    elevation: 0
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(64)

                    MDBoxLayout:
                        spacing: dp(6)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "shield-check"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "18sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "ALERTX MOBILE APK"
                            font_size: "10sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "v0.1.0 (Build 1026100)"
                            font_size: "12sp"
                            bold: True
                            halign: "right"
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                    MDLabel:
                        text: "Production APK Release • Android API 34 • arm64-v8a"
                        font_size: "10sp"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

                MDLabel:
                    text: root.status_text
                    font_size: "13sp"
                    bold: True
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: app.green
                    size_hint_y: None
                    height: dp(24)

        # BOTTOM NAVIGATION BAR (Safety Active)
        MDBoxLayout:
            size_hint_y: None
            height: dp(68)
            theme_bg_color: "Custom"
            md_bg_color: app.surface_lowest
            padding: dp(8), dp(4)

            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_home()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Home"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_contacts()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "card-account-phone"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Contacts"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_safety()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_container
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "shield-check"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"

                    MDLabel:
                        text: "Safety"
                        font_size: "11sp"
                        bold: True
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_primary

            ClickableCard:
                size_hint_x: 0.25
                radius: [0, 0, 0, 0]
                elevation: 0
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                on_release: app.go_help()

                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    spacing: dp(2)

                    MDCard:
                        size_hint: None, None
                        size: dp(54), dp(28)
                        radius: [14, 14, 14, 14]
                        theme_bg_color: "Custom"
                        md_bg_color: [0, 0, 0, 0]
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "information-outline"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"

                    MDLabel:
                        text: "Help"
                        font_size: "11sp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: app.text_secondary


<EmergencyScreen>:
    name: "emergency"

    MDBoxLayout:
        orientation: "vertical"
        theme_bg_color: "Custom"
        md_bg_color: app.bg_surface

        # TOP APP HEADER WITH BACK ARROW
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(12), dp(8)
            spacing: dp(10)
            theme_bg_color: "Custom"
            md_bg_color: app.bg_surface

            ClickableCard:
                size_hint: None, None
                size: dp(38), dp(38)
                radius: [19, 19, 19, 19]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                pos_hint: {"center_y": .5}
                on_release: root.cancel_emergency()

                MDIcon:
                    icon: "arrow-left"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "22sp"

            MDLabel:
                text: "Active SOS Dispatch"
                font_size: "18sp"
                bold: True
                theme_text_color: "Custom"
                text_color: app.text_primary
                pos_hint: {"center_y": .5}

            Widget:

            MDCard:
                size_hint: None, None
                size: dp(34), dp(34)
                radius: [17, 17, 17, 17]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_lowest
                line_color: app.surface_container
                line_width: 1
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "18sp"

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(8), dp(16), dp(44)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # TOP BEACON BANNER (Dark Crimson)
                MDCard:
                    orientation: "vertical"
                    padding: dp(18)
                    spacing: dp(6)
                    radius: [16, 16, 16, 16]
                    elevation: 2
                    theme_bg_color: "Custom"
                    md_bg_color: app.crimson_dark
                    line_color: app.crimson
                    line_width: 1
                    size_hint_y: None
                    height: dp(132)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(26)
                        spacing: dp(8)

                        MDCard:
                            size_hint: None, None
                            size: dp(8), dp(8)
                            radius: [4, 4, 4, 4]
                            pos_hint: {"center_y": .5}
                            theme_bg_color: "Custom"
                            md_bg_color: app.crimson_coral

                        MDLabel:
                            text: "LIVE TRANSMISSION"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.crimson_coral
                            size_hint_x: 1
                            pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint: None, None
                            size: dp(142), dp(26)
                            radius: [13, 13, 13, 13]
                            theme_bg_color: "Custom"
                            md_bg_color: [1, 1, 1, 0.15]
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "access-point"
                                theme_text_color: "Custom"
                                text_color: app.crimson_coral
                                font_size: "15sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Active Uplink"
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.white
                                pos_hint: {"center_y": .5}

                    MDLabel:
                        text: "EMERGENCY ACTIVE"
                        font_size: "24sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.white
                        size_hint_y: None
                        height: dp(32)

                    MDLabel:
                        text: "Alert broadcast initiated at " + root.start_time_text + ". Session ID: #" + root.session_id
                        font_size: "12sp"
                        theme_text_color: "Custom"
                        text_color: [1, 1, 1, 0.85]
                        size_hint_y: None
                        height: dp(20)

                # CARD 1: 1. LOCATION STATUS
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(286)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(32)
                        spacing: dp(8)

                        MDCard:
                            size_hint: None, None
                            size: dp(32), dp(32)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "crosshairs-gps"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "20sp"

                        MDLabel:
                            text: "1. Location Status"
                            font_size: "15sp"
                            bold: True
                            size_hint_x: 1
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint: None, None
                            size: dp(150), dp(26)
                            radius: [13, 13, 13, 13]
                            theme_bg_color: "Custom"
                            md_bg_color: [0.05, 0.29, 0.43, 0.4]
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "check-circle"
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "15sp"
                                size_hint_x: None
                                width: dp(16)
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.location_status
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.blue
                                pos_hint: {"center_y": .5}

                    # Map preview area
                    MDCard:
                        size_hint_y: None
                        height: dp(80)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        padding: dp(10)

                        MDBoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            spacing: dp(4)

                            MDBoxLayout:
                                spacing: dp(6)
                                size_hint_y: None
                                height: dp(22)

                                MDIcon:
                                    icon: "map-marker"
                                    theme_text_color: "Custom"
                                    text_color: app.crimson
                                    font_size: "20sp"

                                MDLabel:
                                    text: "Real GPS Satellite Position"
                                    font_size: "13sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.text_primary

                            MDLabel:
                                text: root.coordinates
                                font_size: "12sp"
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                    # Coordinates & Accuracy 2-column grid
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(66)
                        spacing: dp(10)

                        MDCard:
                            size_hint_x: 0.5
                            orientation: "vertical"
                            padding: dp(8), dp(6)
                            spacing: dp(2)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low

                            MDLabel:
                                text: "COORDINATES"
                                font_size: "9sp"
                                bold: True
                                size_hint_y: None
                                height: dp(14)
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                            MDLabel:
                                text: root.coordinates
                                font_size: "10sp"
                                bold: True
                                shorten: False
                                theme_text_color: "Custom"
                                text_color: app.text_primary

                        MDCard:
                            size_hint_x: 0.5
                            orientation: "vertical"
                            padding: dp(8), dp(6)
                            spacing: dp(2)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low

                            MDLabel:
                                text: "ACCURACY"
                                font_size: "9sp"
                                bold: True
                                size_hint_y: None
                                height: dp(14)
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                            MDLabel:
                                text: root.accuracy_str
                                font_size: "12sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.blue

                    MDBoxLayout:
                        spacing: dp(6)
                        size_hint_y: None
                        height: dp(18)

                        MDIcon:
                            icon: "paperclip"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "15sp"

                        MDLabel:
                            text: "Location payload attached to emergency dispatch"
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary

                # CARD 2: 2. EMERGENCY SMS
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(10)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(278)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(32)
                        spacing: dp(8)

                        MDCard:
                            size_hint: None, None
                            size: dp(32), dp(32)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "message-text"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app.text_primary
                                font_size: "18sp"

                        MDLabel:
                            text: "2. Emergency SMS"
                            font_size: "15sp"
                            bold: True
                            size_hint_x: 1
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint: None, None
                            size: dp(132), dp(26)
                            radius: [13, 13, 13, 13]
                            theme_bg_color: "Custom"
                            md_bg_color: app.green_light
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "check-all"
                                theme_text_color: "Custom"
                                text_color: app.green
                                font_size: "15sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.sms_badge
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.green
                                pos_hint: {"center_y": .5}

                    # Recipient row
                    MDCard:
                        size_hint_y: None
                        height: dp(48)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        padding: dp(8)
                        spacing: dp(10)

                        MDCard:
                            size_hint: None, None
                            size: dp(32), dp(32)
                            radius: [16, 16, 16, 16]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_lowest
                            line_color: app.blue
                            line_width: 1
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.recipient_initials
                                font_size: "13sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.blue

                        MDBoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.recipient_name
                                font_size: "13sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.text_primary

                            MDLabel:
                                text: root.recipient_phone
                                font_size: "11sp"
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                        MDLabel:
                            text: "Just now"
                            font_size: "10sp"
                            halign: "right"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            pos_hint: {"center_y": .5}

                    # Payload quote box
                    MDCard:
                        size_hint_y: None
                        height: dp(80)
                        radius: [8, 8, 8, 8]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_low
                        padding: dp(8)

                        MDLabel:
                            markup: True
                            text: root.sms_payload_markup
                            pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(6)
                        size_hint_y: None
                        height: dp(18)

                        MDIcon:
                            icon: "transmission-tower"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "15sp"

                        MDLabel:
                            text: "SMS cellular network dispatch verified"
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary

                # CARD 3: 3. MONITOR STATE & CALLING
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    line_color: app.surface_container
                    line_width: 1
                    size_hint_y: None
                    height: dp(146)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(32)
                        spacing: dp(8)

                        MDCard:
                            size_hint: None, None
                            size: dp(32), dp(32)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "heart-pulse"
                                pos_hint: {"center_x": .5, "center_y": .5}
                                theme_text_color: "Custom"
                                text_color: app.text_primary
                                font_size: "18sp"

                        MDLabel:
                            text: "3. Monitor State"
                            font_size: "15sp"
                            bold: True
                            size_hint_x: 1
                            theme_text_color: "Custom"
                            text_color: app.text_primary
                            pos_hint: {"center_y": .5}

                        MDCard:
                            size_hint: None, None
                            size: dp(132), dp(26)
                            radius: [13, 13, 13, 13]
                            theme_bg_color: "Custom"
                            md_bg_color: app.crimson_light
                            line_color: app.crimson
                            line_width: 1
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "timer-outline"
                                theme_text_color: "Custom"
                                text_color: app.crimson_coral
                                font_size: "15sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.timer_text
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.crimson_coral
                                pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(56)
                        spacing: dp(10)

                        MDCard:
                            size_hint_x: 0.5
                            padding: dp(8)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            spacing: dp(6)

                            MDIcon:
                                icon: "volume-high"
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "20sp"
                                pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                pos_hint: {"center_y": .5}

                                MDLabel:
                                    text: "Emergency Call"
                                    font_size: "10sp"
                                    theme_text_color: "Custom"
                                    text_color: app.text_secondary

                                MDLabel:
                                    text: root.call_status
                                    font_size: "11sp"
                                    bold: True
                                    shorten: True
                                    theme_text_color: "Custom"
                                    text_color: app.text_primary

                        MDCard:
                            size_hint_x: 0.5
                            padding: dp(8)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low
                            spacing: dp(6)

                            MDIcon:
                                icon: "vibrate"
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "20sp"
                                pos_hint: {"center_y": .5}

                            MDBoxLayout:
                                orientation: "vertical"
                                pos_hint: {"center_y": .5}

                                MDLabel:
                                    text: "Haptics"
                                    font_size: "10sp"
                                    theme_text_color: "Custom"
                                    text_color: app.text_secondary

                                MDLabel:
                                    text: "Continuous SOS"
                                    font_size: "11sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.text_primary

                # PRIMARY ACTION: CANCEL ALERT BUTTON
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(86)
                    spacing: dp(6)

                    ClickableCard:
                        size_hint_y: None
                        height: dp(54)
                        radius: [14, 14, 14, 14]
                        elevation: 2
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_lowest
                        line_color: app.crimson
                        line_width: 1
                        on_touch_down: if self.collide_point(*args[1].pos): root.on_cancel_press()
                        on_touch_up: root.on_cancel_release()

                        MDBoxLayout:
                            spacing: dp(8)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            MDIcon:
                                icon: "close-circle"
                                theme_text_color: "Custom"
                                text_color: app.crimson
                                font_size: "22sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.cancel_status_text
                                font_size: "14sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.crimson
                                pos_hint: {"center_y": .5}

                    MDBoxLayout:
                        spacing: dp(4)
                        size_hint_y: None
                        height: dp(18)
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "information-outline"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "15sp"

                        MDLabel:
                            text: "Cancelling will mark the session resolved and notify contacts you are safe."
                            font_size: "11sp"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
'''


class AlertXApp(MDApp):
    """Main AlertX Personal Safety Application."""

    # Cyber Guardian Dark Safety Theme Color Tokens
    bg_surface = ColorProperty(get_color_from_hex("#0F172A"))
    surface_lowest = ColorProperty(get_color_from_hex("#1E293B"))
    surface_low = ColorProperty(get_color_from_hex("#0F172A"))
    surface_container = ColorProperty(get_color_from_hex("#334155"))
    surface_high = ColorProperty(get_color_from_hex("#475569"))
    surface_highest = ColorProperty(get_color_from_hex("#0284C7"))

    text_primary = ColorProperty(get_color_from_hex("#F8FAFC"))
    text_secondary = ColorProperty(get_color_from_hex("#94A3B8"))

    black = ColorProperty(get_color_from_hex("#0B0F19"))
    white = ColorProperty(get_color_from_hex("#FFFFFF"))
    blue = ColorProperty(get_color_from_hex("#38BDF8"))
    primary_container = ColorProperty(get_color_from_hex("#1E293B"))

    crimson = ColorProperty(get_color_from_hex("#EF4444"))
    crimson_dark = ColorProperty(get_color_from_hex("#450A0A"))
    crimson_coral = ColorProperty(get_color_from_hex("#F87171"))
    crimson_light = ColorProperty(get_color_from_hex("#7F1D1D"))

    green = ColorProperty(get_color_from_hex("#10B981"))
    green_light = ColorProperty(get_color_from_hex("#064E3B"))

    def build(self):
        import traceback
        try:
            self.title = APP_NAME
            self.theme_cls.theme_style = "Dark"

            try:
                Window.softinput_mode = "below_target"
            except Exception:
                pass

            Builder.load_string(KV)

            # Core Safety Services
            self.location = LocationService()
            self.sms = SmsService()
            self.calling = CallingService()
            try:
                from services.api import ApiService
                self.api = ApiService()
            except Exception:
                self.api = None

            self.emergency = EmergencyService(
                self.location,
                self.sms,
                self.calling,
                self.api,
            )

            # Screen Navigation
            self.sm = ScreenManager(transition=FadeTransition(duration=0.15))
            self.sm.add_widget(HomeScreen())
            self.sm.add_widget(ContactsScreen())
            self.sm.add_widget(SettingsScreen())
            self.sm.add_widget(EmergencyScreen())

            return self.sm
        except Exception as exc:
            err = traceback.format_exc()
            print("[CRITICAL ALERTX STARTUP ERROR]", err)
            # Write crash trace to accessible storage for easy diagnosis
            for p in [Path("/sdcard/Download"), Path("/storage/emulated/0/Download"), Path(".")]:
                try:
                    if p.exists():
                        (p / "alertx_crash.txt").write_text(err, encoding="utf-8")
                        break
                except Exception:
                    pass

            # Render an uncrashable pure Kivy error screen
            from kivy.uix.boxlayout import BoxLayout
            from kivy.uix.label import Label
            from kivy.uix.scrollview import ScrollView

            root = BoxLayout(orientation="vertical", padding=20)
            root.add_widget(Label(
                text="[b][color=ff4444]ALERTX LAUNCH ERROR[/color][/b]",
                markup=True,
                size_hint_y=None,
                height=50,
                font_size="18sp"
            ))
            sv = ScrollView()
            sv.add_widget(Label(
                text=err,
                size_hint_y=None,
                height=1500,
                text_size=(750, None),
                halign="left",
                valign="top"
            ))
            root.add_widget(sv)
            return root

    def on_start(self):
        """Schedule hardware back button binding and passive system checks."""
        try:
            Window.bind(on_keyboard=self._on_keyboard)
        except Exception:
            pass

        # Passively start location listening only if permissions are already granted
        try:
            from native_platform.native_bridge import is_android, check_permission
            if is_android() and (check_permission("ACCESS_FINE_LOCATION") or check_permission("ACCESS_COARSE_LOCATION")):
                if hasattr(self, "location") and self.location:
                    self.location.start_gps()
        except Exception:
            pass

    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        """Handle Android hardware back button (keycode 27)."""
        if key == 27:
            if hasattr(self, "sm") and self.sm:
                current = self.sm.current
                if current in ("contacts", "safety"):
                    self.go_home()
                    return True
                elif current == "emergency":
                    # In emergency, do not allow hardware back button to silently abort crisis dispatch
                    return True
                elif current == "home":
                    # Allow normal Android back/minimize
                    return False
        return False

    def on_pause(self):
        """Allow app to stay alive when minimized or phone screen turns off."""
        return True

    def on_resume(self):
        """Called when app returns from background."""
        pass

    def go_home(self, *args):
        self.sm.current = "home"
        if self.sm.has_screen("home"):
            self.sm.get_screen("home").refresh()

    def go_contacts(self, *args):
        self.sm.current = "contacts"
        if self.sm.has_screen("contacts"):
            self.sm.get_screen("contacts").load_contact()

    def go_safety(self, *args):
        self.sm.current = "safety"
        if self.sm.has_screen("safety"):
            self.sm.get_screen("safety").refresh()

    def go_help(self, *args):
        self.go_safety()

    def start_emergency(self):
        try:
            from native_platform.native_bridge import is_android, has_all_emergency_permissions, request_emergency_permissions
            if is_android() and not has_all_emergency_permissions():
                request_emergency_permissions(lambda perms, results: self._refresh_emergency_after_perms())
        except Exception:
            pass

        result = self.emergency.activate()
        emergency_screen = self.sm.get_screen("emergency")
        emergency_screen.apply_result(result)
        self.sm.current = "emergency"

    def _refresh_emergency_after_perms(self):
        """Update live telemetry if permissions were granted after SOS press."""
        if hasattr(self, "sm") and self.sm and self.sm.current == "emergency":
            emergency_screen = self.sm.get_screen("emergency")
            if hasattr(self, "location"):
                loc = self.location.get_current()
                if loc.get("ok"):
                    emergency_screen.coordinates = loc.get("coordinates_str", emergency_screen.coordinates)
                    emergency_screen.location_status = loc.get("status", emergency_screen.location_status)
                    emergency_screen.accuracy_str = loc.get("accuracy_str", emergency_screen.accuracy_str)


# =============================================================================
# Bulletproof Exception Handling: Keep App Alive Under All Runtime Errors
# =============================================================================
import traceback
import threading
from kivy.base import ExceptionManager, ExceptionHandler


def _log_unhandled_crash(err: str):
    """Write crash trace to disk and Android Logcat so it never vanishes."""
    print("[CRITICAL EXCEPTION INTERCEPTED]", err)
    try:
        from jnius import autoclass
        Log = autoclass("android.util.Log")
        Log.e("AlertXCrash", err)
    except Exception:
        pass
    for p in [Path("/sdcard/Download"), Path("/storage/emulated/0/Download"), Path(".")]:
        try:
            if p.exists():
                (p / "alertx_crash.txt").write_text(err, encoding="utf-8")
                break
        except Exception:
            pass


class AlertXExceptionHandler(ExceptionHandler):
    """Intercept all unhandled Kivy clock/event exceptions and keep app alive."""

    def handle_exception(self, inst):
        err = traceback.format_exc()
        _log_unhandled_crash(err)
        return ExceptionManager.PASS  # Keeps app alive without closing!


def _global_excepthook(exc_type, exc_value, exc_traceback):
    err = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    _log_unhandled_crash(err)


def _threading_excepthook(args):
    _global_excepthook(args.exc_type, args.exc_value, args.exc_traceback)


try:
    ExceptionManager.add_handler(AlertXExceptionHandler())
except Exception:
    pass

sys.excepthook = _global_excepthook
threading.excepthook = _threading_excepthook


if __name__ == "__main__":
    AlertXApp().run()