from typing import Any, List


class Observer:
    def update(self, event: str, *args: Any, **kwargs: Any) -> None:
        pass


class Observable:
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def register_observer(self, observer: Observer) -> None:
        """Registers an observer to receive notifications."""
        self._observers.append(observer)

    def unregister_observer(self, observer: Observer) -> None:
        """Removes an observer from the notification list."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Notifies all registered observers of an event."""
        for observer in self._observers:
            observer.update(event, *args, **kwargs)
