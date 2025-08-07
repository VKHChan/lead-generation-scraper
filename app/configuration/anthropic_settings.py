from pydantic.dataclasses import dataclass

from .configurable_settings import ConfigurableSettings

"""
similarly we can create settings for azure and aws
@dataclass
class AzureSettings:
    deployment_name: str
    endpoint: str
    api_version: str = "2023-05-15"

@dataclass
class AWSSettings:
    region: str
    role_arn: str | None = None
"""


@dataclass
class AnthropicSettings(ConfigurableSettings):

    def __init__(self, values: dict[str, str | None]):
        self._api_key = values.get("ANTHROPIC_API_KEY")

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def is_configured(self) -> bool:
        return self._api_key is not None
