from .configurable_settings import ConfigurableSettings


class LocalSettings(ConfigurableSettings):
    """
    Settings for the local.
    """

    def __init__(self, values: dict[str, str | None]):
        self._local_storage_path = values.get(
            "LOCAL_STORAGE_PATH") or "workspace/storage"

    @property
    def local_storage_path(self) -> str:
        return self._local_storage_path

    @property
    def is_configured(self) -> bool:
        return self._local_storage_path is not None
