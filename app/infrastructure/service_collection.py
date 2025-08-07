from typing import Type

from injector import Binder, Injector, Module, T, singleton

from app.configuration.settings import Settings, get_settings
from app.core.storage import Storage
from app.infrastructure.local_services import LocalModule
from app.infrastructure.web_scrape_services import WebScraperModule
from app.infrastructure.web_search_services import WebSearchModule


class ApplicationModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(Settings, to=get_settings, scope=singleton)


class ServiceProvider:
    _injector: Injector | None = None
    _instance: "ServiceProvider | None" = None

    @classmethod
    def _initialize(cls, injector: Injector) -> "ServiceProvider":
        if cls._instance is None:
            cls._instance = cls()
        cls._instance._injector = injector
        return cls._instance

    @classmethod
    def get(cls, service_type: Type[T]) -> T:
        if cls._instance is None or cls._instance._injector is None:
            raise Exception("Services not initialized.")
        return cls._instance._injector.get(service_type)

    @classmethod
    def get_injector(cls) -> Injector:
        if cls._instance is None or cls._instance._injector is None:
            raise Exception("Services not initialized.")
        return cls._instance._injector

    @classmethod
    def is_initialized(cls) -> bool:
        return cls._instance is not None and cls._instance._injector is not None


class ServiceCollection:
    """A collection of services for the application."""
    @staticmethod
    def add_services() -> ServiceProvider:
        settings = get_settings()
        modules = [
            ApplicationModule(),
            WebSearchModule(
                search_engine=settings.web_search_settings.search_engine),
            WebScraperModule(),
        ]
        if settings.local_settings.is_configured:
            modules.append(LocalModule(app_host=settings.app_host))

        injector = Injector(modules=modules)
        return ServiceProvider._initialize(injector)
