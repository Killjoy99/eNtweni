# A service locator class where services like connection manager can subscribe to and share data


class ServiceLocator:
    _services: dict = {}

    @classmethod
    def register_service(cls, service_name, service_instance):
        cls._services[service_name] = service_instance

    @classmethod
    def get_service(cls, service_name):
        return cls._services.get(service_name)
