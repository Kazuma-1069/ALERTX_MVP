import sys
from pathlib import Path

# Ensure app directory is on path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

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


KV = '''
#:import dp kivy.metrics.dp

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
                md_bg_color: app.black
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=10sp][color=0051D5]ALERTX[/color][/size][/b]  [size=14sp][color=0051D5]•[/color][/size]\\n[b][size=18sp][color=0B1C30]Home[/color][/size][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            # Online capsule badge
            MDCard:
                size_hint: None, None
                size: dp(88), dp(28)
                radius: [self.height / 2, self.height / 2, self.height / 2, self.height / 2]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_container
                padding: dp(8), dp(4)
                spacing: dp(6)
                pos_hint: {"center_y": .5}

                MDCard:
                    size_hint: None, None
                    size: dp(6), dp(6)
                    radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                    pos_hint: {"center_y": .5}
                    theme_bg_color: "Custom"
                    md_bg_color: app.blue

                MDLabel:
                    text: "ONLINE"
                    font_size: "10sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app.text_secondary
                    pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(34), dp(34)
                radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                theme_bg_color: "Custom"
                md_bg_color: app.black
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "18sp"

        # SCROLLABLE CONTENT
        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(6), dp(16), dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # ALERTX PRO / ARMED BANNER
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(52)
                    spacing: dp(10)

                    MDCard:
                        size_hint: None, None
                        size: dp(46), dp(46)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.primary_container
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
                        size: dp(106), dp(30)
                        radius: [15, 15, 15, 15]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_high
                        padding: dp(8), dp(4)
                        spacing: dp(6)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "shield-check"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "ARMED"
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.text_primary
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
                        md_bg_color: app.surface_low
                        padding: dp(8), dp(2)
                        spacing: dp(4)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "check-circle"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "16sp"
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: root.contact_badge
                            font_size: "11sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: app.blue
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
                            icon: "map-marker"
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
                        md_bg_color: app.surface_low
                        padding: dp(8), dp(2)
                        spacing: dp(4)
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "checkbox-marked-circle-outline"
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

                    # Circular Outer Aura, White Highlight Ring & SOS Button
                    AnchorLayout:
                        anchor_x: "center"
                        anchor_y: "center"
                        size_hint_y: None
                        height: dp(246)

                        # Outer Soft Aura (Pink/Reddish)
                        MDCard:
                            size_hint: None, None
                            size: dp(234), dp(234)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            theme_bg_color: "Custom"
                            md_bg_color: [0.73, 0.10, 0.10, 0.08]

                        # White Highlight Ring
                        MDCard:
                            size_hint: None, None
                            size: dp(198), dp(198)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            theme_bg_color: "Custom"
                            md_bg_color: [1, 1, 1, 0.95]
                            elevation: 1

                        # Main Crimson SOS Button
                        ClickableCard:
                            size_hint: None, None
                            size: dp(184), dp(184)
                            radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                            elevation: 4
                            theme_bg_color: "Custom"
                            md_bg_color: app.crimson
                            on_release: root.trigger_sos()

                            MDBoxLayout:
                                orientation: "vertical"
                                padding: dp(14), dp(12)
                                spacing: dp(2)
                                pos_hint: {"center_x": .5, "center_y": .5}

                                AnchorLayout:
                                    anchor_x: "center"
                                    anchor_y: "center"
                                    size_hint_y: None
                                    height: dp(48)

                                    MDCard:
                                        size_hint: None, None
                                        size: dp(48), dp(48)
                                        radius: [self.width / 2, self.width / 2, self.width / 2, self.width / 2]
                                        theme_bg_color: "Custom"
                                        md_bg_color: [1, 1, 1, 0.18]

                                        AnchorLayout:
                                            anchor_x: "center"
                                            anchor_y: "center"

                                            MDIcon:
                                                icon: "power"
                                                theme_text_color: "Custom"
                                                text_color: app.white
                                                font_size: "26sp"

                                MDLabel:
                                    text: "SOS"
                                    font_size: "38sp"
                                    bold: True
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: app.white
                                    size_hint_y: None
                                    height: dp(42)

                                MDLabel:
                                    text: "EMERGENCY"
                                    font_size: "10sp"
                                    bold: True
                                    halign: "center"
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 0.9]
                                    size_hint_y: None
                                    height: dp(16)

                    # Info Badge below button
                    MDCard:
                        size_hint: None, None
                        size: dp(260), dp(32)
                        radius: [self.height / 2, self.height / 2, self.height / 2, self.height / 2]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_high
                        padding: dp(12), dp(4)
                        spacing: dp(6)
                        pos_hint: {"center_x": .5}

                        MDIcon:
                            icon: "gesture-tap"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "16sp"
                            size_hint_x: None
                            width: dp(16)
                            pos_hint: {"center_y": .5}

                        MDLabel:
                            text: "Hold 2s to Prevent False Alarms"
                            font_size: "10sp"
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
                    md_bg_color: app.surface_low
                    size_hint_y: None
                    height: dp(112)

                    MDCard:
                        size_hint: None, None
                        size: dp(40), dp(40)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_highest
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
                        font_size: "14sp"
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
                        md_bg_color: app.surface_highest
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
                md_bg_color: app.black
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=10sp][color=0051D5]ALERTX[/color][/size][/b]  [size=14sp][color=0051D5]•[/color][/size]\\n[b][size=18sp][color=0B1C30]Emergency Contacts[/color][/size][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(96), dp(28)
                radius: [14, 14, 14, 14]
                theme_bg_color: "Custom"
                md_bg_color: app.surface_container
                padding: dp(8), dp(4)
                spacing: dp(6)
                pos_hint: {"center_y": .5}

                MDCard:
                    size_hint: None, None
                    size: dp(8), dp(8)
                    radius: [4, 4, 4, 4]
                    pos_hint: {"center_y": .5}
                    theme_bg_color: "Custom"
                    md_bg_color: app.blue

                MDLabel:
                    text: "ONLINE"
                    font_size: "11sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app.blue
                    pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(34), dp(34)
                radius: [17, 17, 17, 17]
                theme_bg_color: "Custom"
                md_bg_color: app.black
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "20sp"

        # SCROLLABLE CONTENT
        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(8), dp(16), dp(20)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height

                # SCREEN INTRO
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(80)
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
                        height: dp(54)

                # AUTOMATED SOS PROTOCOL INFO CARD
                MDCard:
                    orientation: "horizontal"
                    padding: dp(14)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 0
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_low
                    size_hint_y: None
                    height: dp(100)

                    MDCard:
                        size_hint: None, None
                        size: dp(42), dp(42)
                        radius: [10, 10, 10, 10]
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_highest
                        pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "email-outline"
                            pos_hint: {"center_x": .5, "center_y": .5}
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "22sp"

                    MDLabel:
                        markup: True
                        text: root.automated_sos_markup
                        font_size: "14sp"
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
                            size: dp(86), dp(22)
                            radius: [11, 11, 11, 11]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_highest
                            padding: dp(8), dp(2)
                            spacing: dp(4)

                            MDCard:
                                size_hint: None, None
                                size: dp(6), dp(6)
                                radius: [3, 3, 3, 3]
                                pos_hint: {"center_y": .5}
                                theme_bg_color: "Custom"
                                md_bg_color: app.blue

                            MDLabel:
                                text: "Primary"
                                font_size: "11sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.blue

                    MDCard:
                        orientation: "vertical"
                        padding: dp(16)
                        spacing: dp(14)
                        radius: [16, 16, 16, 16]
                        elevation: 1
                        theme_bg_color: "Custom"
                        md_bg_color: app.surface_lowest
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
                                md_bg_color: app.primary_container
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
                                    text_color: app.blue
                                    font_size: "18sp"

                                MDLabel:
                                    text: "Verified for SMS alerts"
                                    font_size: "12sp"
                                    bold: True
                                    theme_text_color: "Custom"
                                    text_color: app.blue

                            ClickableCard:
                                size_hint: None, None
                                size: dp(120), dp(32)
                                radius: [16, 16, 16, 16]
                                theme_bg_color: "Custom"
                                md_bg_color: app.surface_container
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
                            icon: "badge-account-horizontal"
                            theme_text_color: "Custom"
                            text_color: app.text_secondary
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}

                        TextInput:
                            id: name_field
                            text: "Sarah Jenkins"
                            background_color: [0, 0, 0, 0]
                            foreground_color: [0.04, 0.11, 0.19, 1]
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
                            md_bg_color: app.black if root.selected_relation == "Parent" else app.surface_low
                            on_release: root.select_relation("Parent")

                            MDLabel:
                                text: "Parent"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.white if root.selected_relation == "Parent" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.black if root.selected_relation == "Spouse" else app.surface_low
                            on_release: root.select_relation("Spouse")

                            MDLabel:
                                text: "Spouse"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.white if root.selected_relation == "Spouse" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.black if root.selected_relation == "Sibling" else app.surface_low
                            on_release: root.select_relation("Sibling")

                            MDLabel:
                                text: "Sibling"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.white if root.selected_relation == "Sibling" else app.text_secondary

                        ClickableCard:
                            size_hint_x: 0.25
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.black if root.selected_relation == "Friend" else app.surface_low
                            on_release: root.select_relation("Friend")

                            MDLabel:
                                text: "Friend"
                                font_size: "12sp"
                                bold: True
                                halign: "center"
                                theme_text_color: "Custom"
                                text_color: app.white if root.selected_relation == "Friend" else app.text_secondary

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
                            background_color: [0, 0, 0, 0]
                            foreground_color: [0.04, 0.11, 0.19, 1]
                            font_size: "15sp"
                            multiline: False
                            pos_hint: {"center_y": .5}

                        MDIcon:
                            icon: "check-circle"
                            theme_text_color: "Custom"
                            text_color: app.blue
                            font_size: "20sp"
                            pos_hint: {"center_y": .5}

                    # Save Contact Button
                    ClickableCard:
                        size_hint_y: None
                        height: dp(50)
                        radius: [12, 12, 12, 12]
                        theme_bg_color: "Custom"
                        md_bg_color: app.black
                        padding: dp(12), dp(4)
                        spacing: dp(8)
                        on_release: root.save_contact()

                        MDBoxLayout:
                            spacing: dp(8)
                            pos_hint: {"center_x": .5, "center_y": .5}

                            MDIcon:
                                icon: "content-save"
                                theme_text_color: "Custom"
                                text_color: app.white
                                font_size: "20sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: "Save Contact"
                                font_size: "15sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.white
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
                            md_bg_color: app.surface_highest
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "map-marker"
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
                            md_bg_color: app.surface_highest
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
                        md_bg_color: app.surface_highest
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
                md_bg_color: app.black
                padding: dp(8)
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "shield-outline"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "24sp"

            MDLabel:
                markup: True
                text: "[b][size=10sp][color=0051D5]ALERTX[/color][/size][/b]  [size=14sp][color=0051D5]•[/color][/size]\\n[b][size=18sp][color=0B1C30]Safety & SOS Settings[/color][/size][/b]"
                size_hint_x: 1
                pos_hint: {"center_y": .5}

            MDCard:
                size_hint: None, None
                size: dp(34), dp(34)
                radius: [17, 17, 17, 17]
                theme_bg_color: "Custom"
                md_bg_color: app.black
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "20sp"

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
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
                        md_bg_color: app.surface_container
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
                        on_release: root.reset_template()

                        MDLabel:
                            text: "Restore Default SOS Template"
                            font_size: "12sp"
                            bold: True
                            halign: "center"
                            theme_text_color: "Custom"
                            text_color: app.blue

                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    radius: [16, 16, 16, 16]
                    elevation: 1
                    theme_bg_color: "Custom"
                    md_bg_color: app.surface_lowest
                    size_hint_y: None
                    height: dp(180)

                    MDLabel:
                        text: "SYSTEM & HARDWARE STATUS"
                        font_size: "11sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.text_secondary

                    MDBoxLayout:
                        spacing: dp(8)
                        MDIcon:
                            icon: "map-marker-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                        MDLabel:
                            text: "GPS Location Receiver: Ready (High Accuracy)"
                            font_size: "13sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary

                    MDBoxLayout:
                        spacing: dp(8)
                        MDIcon:
                            icon: "message-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                        MDLabel:
                            text: "Cellular SMS Telephony: Active"
                            font_size: "13sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary

                    MDBoxLayout:
                        spacing: dp(8)
                        MDIcon:
                            icon: "phone-check"
                            theme_text_color: "Custom"
                            text_color: app.green
                            font_size: "20sp"
                        MDLabel:
                            text: "Emergency Calling Dispatch: Armed"
                            font_size: "13sp"
                            theme_text_color: "Custom"
                            text_color: app.text_primary

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
                        md_bg_color: app.surface_highest
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
                md_bg_color: app.surface_low
                pos_hint: {"center_y": .5}
                on_release: root.cancel_emergency()

                MDIcon:
                    icon: "arrow-left"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.text_primary
                    font_size: "22sp"

            MDLabel:
                text: "Active Sos Dispatch"
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
                md_bg_color: app.black
                pos_hint: {"center_y": .5}

                MDIcon:
                    icon: "account"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    theme_text_color: "Custom"
                    text_color: app.white
                    font_size: "18sp"

        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16), dp(8), dp(16), dp(24)
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
                    size_hint_y: None
                    height: dp(270)

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(32)
                        spacing: dp(8)

                        MDCard:
                            size_hint: None, None
                            size: dp(32), dp(32)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_highest
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
                            md_bg_color: app.surface_low
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
                        md_bg_color: app.surface_container
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
                        height: dp(56)
                        spacing: dp(10)

                        MDCard:
                            size_hint_x: 0.5
                            orientation: "vertical"
                            padding: dp(8)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low

                            MDLabel:
                                text: "COORDINATES"
                                font_size: "9sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.text_secondary

                            MDLabel:
                                text: root.coordinates
                                font_size: "12sp"
                                bold: True
                                shorten: True
                                theme_text_color: "Custom"
                                text_color: app.text_primary

                        MDCard:
                            size_hint_x: 0.5
                            orientation: "vertical"
                            padding: dp(8)
                            radius: [8, 8, 8, 8]
                            theme_bg_color: "Custom"
                            md_bg_color: app.surface_low

                            MDLabel:
                                text: "ACCURACY"
                                font_size: "9sp"
                                bold: True
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
                            md_bg_color: app.surface_high
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
                            md_bg_color: app.surface_low
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "check-all"
                                theme_text_color: "Custom"
                                text_color: app.blue
                                font_size: "15sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.sms_badge
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.blue
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
                            md_bg_color: app.surface_highest
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
                        md_bg_color: app.surface_container
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
                            md_bg_color: app.surface_high
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
                            padding: dp(6), dp(2)
                            spacing: dp(4)
                            pos_hint: {"center_y": .5}

                            MDIcon:
                                icon: "timer-outline"
                                theme_text_color: "Custom"
                                text_color: app.crimson
                                font_size: "15sp"
                                pos_hint: {"center_y": .5}

                            MDLabel:
                                text: root.timer_text
                                font_size: "10sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: app.crimson
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
                        on_release: root.cancel_emergency()

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
                                text: "HOLD TO CANCEL ALERT"
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

    # Color tokens from guardian_modern/DESIGN.md
    bg_surface = ColorProperty(get_color_from_hex("#F8F9FF"))
    surface_lowest = ColorProperty(get_color_from_hex("#FFFFFF"))
    surface_low = ColorProperty(get_color_from_hex("#EFF4FF"))
    surface_container = ColorProperty(get_color_from_hex("#E5EEFF"))
    surface_high = ColorProperty(get_color_from_hex("#DCE9FF"))
    surface_highest = ColorProperty(get_color_from_hex("#D3E4FE"))

    text_primary = ColorProperty(get_color_from_hex("#0B1C30"))
    text_secondary = ColorProperty(get_color_from_hex("#45464D"))

    black = ColorProperty(get_color_from_hex("#000000"))
    white = ColorProperty(get_color_from_hex("#FFFFFF"))
    blue = ColorProperty(get_color_from_hex("#0051D5"))
    primary_container = ColorProperty(get_color_from_hex("#131B2E"))

    crimson = ColorProperty(get_color_from_hex("#DC2626"))
    crimson_dark = ColorProperty(get_color_from_hex("#410002"))
    crimson_coral = ColorProperty(get_color_from_hex("#F63A35"))
    crimson_light = ColorProperty(get_color_from_hex("#FFDAD6"))

    green = ColorProperty(get_color_from_hex("#059669"))
    green_light = ColorProperty(get_color_from_hex("#ECFDF5"))

    def build(self):
        self.title = APP_NAME
        self.theme_cls.theme_style = "Light"

        Builder.load_string(KV)

        # Core Safety Services
        self.location = LocationService()
        self.sms = SmsService()
        self.calling = CallingService()
        self.emergency = EmergencyService(
            self.location,
            self.sms,
            self.calling,
        )

        # Screen Navigation
        self.sm = ScreenManager(transition=FadeTransition(duration=0.15))
        self.sm.add_widget(HomeScreen())
        self.sm.add_widget(ContactsScreen())
        self.sm.add_widget(SettingsScreen())
        self.sm.add_widget(EmergencyScreen())

        return self.sm

    def on_start(self):
        """Schedule runtime Android permissions after window is ready."""
        from kivy.clock import Clock
        try:
            from native_platform.native_bridge import request_emergency_permissions
            Clock.schedule_once(lambda dt: request_emergency_permissions(), 0.5)
        except Exception as exc:
            print(f"[AlertX] Permission bridge error: {exc}")

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
        result = self.emergency.activate()
        emergency_screen = self.sm.get_screen("emergency")
        emergency_screen.apply_result(result)
        self.sm.current = "emergency"


if __name__ == "__main__":
    AlertXApp().run()