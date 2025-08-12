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


class AnthropicSettings(ConfigurableSettings):
    api_key: str | None = None

    def __init__(self, values: dict[str, str | None]):
        self.api_key = values.get("ANTHROPIC_API_KEY") or ""

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)
