from injector import Binder, Module, inject, singleton
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

from app.configuration.settings import Settings
from app.core.domain import ChatModelProvider, ModelHost

"""
We could create a similar services for azure, and other cloud providers.

For example, if we want to use azure storage, we could create a AzureStorage similar to LocalStorage,
and bind it to the Storage interface if app_host is azure.
And we can create a ChatModelProvider for azure, and bind it to the ChatModelProvider interface if llm_model_host is azure.

The same for other cloud providers.
"""


class AnthropicModule(Module):
    def __init__(self, llm_model_host: str):
        self.llm_model_host = llm_model_host

    def configure(self, binder: Binder) -> None:
        if self.llm_model_host == ModelHost.ANTHROPIC:
            binder.bind(ChatModelProvider,
                        to=AnthropicChatModelProvider,
                        scope=singleton
                        )


class AnthropicChatModelProvider(ChatModelProvider):
    @inject
    def __init__(self, settings: Settings):
        self._settings = settings

    def can_handle(self) -> bool:
        return self._settings.llm_settings.chat_model_settings.host == ModelHost.ANTHROPIC

    def get_chat_model(self) -> BaseChatModel:
        return ChatAnthropic(
            model=self._settings.llm_settings.chat_model_settings.model_name,
            api_key=self._settings.anthropic.api_key,
            temperature=self._settings.llm_settings.chat_model_settings.temperature,
            top_p=self._settings.llm_settings.chat_model_settings.top_p,
            max_tokens=self._settings.llm_settings.chat_model_settings.max_tokens,
            streaming=self._settings.llm_settings.chat_model_settings.streaming,
            force_tool_support=self._settings.llm_settings.chat_model_settings.force_tool_support,
        )
