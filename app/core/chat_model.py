from core.domain import ChatModelSettings
from langchain_core.language_models.chat_models import BaseChatModel


class ChatModelProvider:

    def can_handle(self, chat_model_settings: ChatModelSettings) -> bool:
        raise NotImplementedError

    def get_chat_model(
        self,
        chat_model_settings: ChatModelSettings,
        verbose: bool = False,
    ) -> BaseChatModel:
        raise NotImplementedError
