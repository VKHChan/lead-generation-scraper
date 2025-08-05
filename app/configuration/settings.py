import os

import dotenv
from dotenv import dotenv_values

from .local_settings import LocalSettings
from .web_search_settings import WebSearchSettings

dotenv.load_dotenv()


class Settings:
    _instance = None

    @staticmethod
    def instance(dotenv_path: str = "") -> "Settings":
        if Settings._instance is None:
            Settings(dotenv_path)
        else:
            Settings._instance._settings.update(os.environ)
        return Settings._instance

    def __init__(self, dotenv_path: str = ""):
        if Settings._instance is not None:
            raise Exception(
                "This class can only be a singleton. Use get_instance() to get the instance"
            )
        else:
            Settings._instance = self

        self._settings = self.__get_dotenv_settings(dotenv_path=dotenv_path)
        self._settings.update(os.environ)
        self._app_host = self._settings.get("APP_HOST") or "local"
        self._web_search_settings = WebSearchSettings(self._settings)
        self._local_settings = LocalSettings(self._settings)

    def __get_dotenv_settings(self, dotenv_path: str = "") -> dict[str, str | None]:
        config = dotenv_values()
        dotenv_file = f"{dotenv_path}.env"
        config.update(dotenv_values(dotenv_file))
        keys_dotenv_file = f"{dotenv_path}.env.keys"
        if (os.path.exists(keys_dotenv_file)):
            config.update(dotenv_values(keys_dotenv_file))
        return config

    def __resolve_bool(self, value: str | None) -> bool:
        return (value or "").lower() == "true"

    @property
    def local_settings(self) -> LocalSettings:
        return self._local_settings

    @property
    def web_search_settings(self) -> WebSearchSettings:
        return self._web_search_settings

    @property
    def app_host(self) -> str:
        return self._app_host


def get_settings(
    dotenv_path: str = "",
) -> Settings:
    if not dotenv_path:
        current_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(current_dir, '../')

    return Settings.instance(dotenv_path=dotenv_path)
