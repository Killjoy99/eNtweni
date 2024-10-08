import cProfile  # noqa: F401
import logging

from kivy.core.window import Window
from kivy.utils import platform
from kivymd.app import MDApp

# Import the optimized Root class
# from libs.uix.optimised_root import Root
from libs.uix.root import Root

logging.basicConfig(level=logging.INFO)


class EntweniBooking(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Entweni Booking"
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"

    def build(self):
        # Set window size only if running on non-Android platforms

        if platform != "android":
            Window.size = (420, 840)

        # Register the services for later referencing from all screens
        # Initialize the root widget
        self.root = Root()
        self.root.push("welcome")


if __name__ == "__main__":
    # Start the kivy application
    EntweniBooking().run()
