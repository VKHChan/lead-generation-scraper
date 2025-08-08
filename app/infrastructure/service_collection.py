from typing import Type

from configuration.settings import Settings, get_settings
from infrastructure.anthropic_services import AnthropicModule
from infrastructure.local_services import LocalModule
from infrastructure.web_scrape_services import WebScraperModule
from infrastructure.web_search_services import WebSearchModule
from injector import Binder, Injector, Module, T, singleton


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
                search_engine=settings.web_search_settings.search_engine
            ),
            WebScraperModule(),
        ]
        if settings.local_settings.is_configured:
            modules.append(LocalModule(app_host=settings.app_host))
        if settings.anthropic.is_configured:
            modules.append(AnthropicModule(
                llm_model_host=settings.llm_settings.chat_model_settings.host
            ))

        injector = Injector(modules=modules)
        return ServiceProvider._initialize(injector)
