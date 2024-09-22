import logging

import httpx
from libs.applibs.services.observable import Observable

logger = logging.getLogger(__name__)


class ConnectionManager(Observable):
    def __init__(self):
        super().__init__()
        self.is_connected = False
        self.client = (
            httpx.Client()
        )  # Use httpx.AsyncClient() if you want async behavior

    def connect(self) -> None:
        """Simulate connecting and notify observers."""
        # Connection logic here
        self.is_connected = True
        self.notify_observers("Connected")
        logger.info("Connected to the server.")

    def disconnect(self) -> None:
        """Simulate disconnecting and notify observers."""
        # Disconnection logic here
        if self.client:
            self.client.close()
        self.is_connected = False
        self.notify_observers("Disconnected")
        logger.info("Disconnected from the server.")

    def fetch_data(self, url: str) -> dict:
        """Fetch data from the API."""
        if not self.is_connected:
            logger.error("Cannot fetch data: Not connected.")
            return {}

        try:
            response = self.client.get(url)  # Use async method if using AsyncClient
            response.raise_for_status()  # Raise an error for bad responses
            logger.info(f"Data fetched from {url}: {response.json()}")
            return response  # Return the response data as a dictionary
        except httpx.RequestError as e:
            logger.error(f"An error occurred while requesting data: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")

        return {}
