from typing import Any, Dict

from app.core.domain import ChatModelSettings


class LLMSettings:
    _instance = None

    def __init__(self, values: dict[str, Any]):

        self._chat_model_settings = ChatModelSettings(
            host=values.get("LLM_HOST", ""),
            provider=values.get("LLM_PROVIDER", ""),
            model_name=values.get("LLM_MODEL_NAME", ""),
            streaming=values.get("LLM_STREAMING", "true").lower() == "true",
            force_tool_support=values.get(
                "LLM_FORCE_TOOL_SUPPORT", "false").lower() == "true",
            temperature=float(values.get("LLM_TEMPERATURE", "0.7")),
            top_p=float(values.get("LLM_TOP_P", "0.95")),
            max_tokens=int(values.get("LLM_MAX_TOKENS", "0")) or None,
        )

    @property
    def chat_model_settings(self) -> ChatModelSettings:
        return self._chat_model_settings
