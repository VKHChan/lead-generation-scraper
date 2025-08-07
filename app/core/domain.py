from dataclasses import asdict, fields
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic.dataclasses import Field, dataclass


class ModelHost:
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    AWS = "aws"


class ModelProvider:
    ANTHROPIC = "anthropic"


@dataclass
class BaseSettings:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def get_keys(cls) -> list[str]:
        return [f.name for f in fields(cls)]


@dataclass(frozen=True)
class ChatModelSettings:
    host: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    model_name: str = Field(..., min_length=1)
    streaming: bool = True
    force_tool_support: bool = False
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int | None = None


class ChatModelProvider:
    def can_handle(self, chat_model_settings: ChatModelSettings) -> bool:
        raise NotImplementedError

    def get_chat_model(
        self,
        chat_model_settings: ChatModelSettings,
        verbose: bool = False,
    ) -> BaseChatModel:
        raise NotImplementedError
