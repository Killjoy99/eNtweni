import logging

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen
from libs.applibs.services.connection_manager import ConnectionManager
from libs.applibs.services.observable import Observer
from libs.applibs.services.service_locator import ServiceLocator

logger = logging.getLogger(__name__)


class WelcomeScreen(MDScreen, Observer):
    name: str = StringProperty("")
    status: str = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Store services in instance variables to avoid multiple lookups
        self.connection_manager = None
        self.shared_data_service = None

        try:
            # Retrieve connection manager service
            self.connection_manager = ServiceLocator.get_service("connection_manager")
            self.connection_manager.register_observer(self)

            # Retrieve shared data service
            self.shared_data_service = ServiceLocator.get_service("shared_data")
            self.shared_data_service.register_observer(self)
        except KeyError as e:
            logger.error(f"Service not found: {e}")

    # def on_enter(self):
    #     """Called when the screen is displayed."""
    #     self.connect_to_google()

    def change_name(self, new_name: str) -> None:
        logger.info(f"Changing name to: {new_name}")
        self.name = new_name  # This updates the UI dynamically
        self.manager.set_shared_data("name", new_name)

        # notify the observers
        self.notify_observers("name", new_name)

    def on_leave(self):
        """Unregister observers and disconnect when leaving the screen."""
        try:
            # Unregister observers to avoid memory leaks
            if self.connection_manager:
                self.connection_manager.unregister_observer(self)
                self.connection_manager.disconnect()
            if self.shared_data_service:
                self.shared_data_service.unregister_observer(self)
        except KeyError as e:
            logger.error(f"Service not found during exit: {e}")

    def connect_to_google(self):
        conn_manager = ConnectionManager()
        conn_manager.connect()  # connect to the server
        data = conn_manager.fetch_data("https://www.goog.com/")
        self.status = data.json()
        print(data.json().get("Set-Cookie"))

        conn_manager.disconnect()
