from typing import Any

from .observable import Observable


class SharedDataService(Observable):
    def __init__(self) -> None:
        super().__init__()
        self._data = {}

    def set_data(self, key: str, value: Any) -> None:
        """Sets a key-value pair in shared data and notifies observers."""
        self._data[key] = value
        # Notify observers with a dictionary containing key and value
        self.notify_observers({"key": key, "value": value})

    def get_data(self, key: str) -> Any:
        """Gets the value associated with the key in shared data."""
        return self._data.get(key, None)
