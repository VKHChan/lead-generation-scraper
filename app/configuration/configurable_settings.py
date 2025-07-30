from typing import Protocol


class ConfigurableSettings(Protocol):
    @property
    def is_configured(self) -> bool:
        """Indicates if the settings are properly configured."""
        ...
