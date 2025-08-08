from core.chat_model import ChatModelProvider
from core.domain import ContentAnalysis
from injector import inject
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from .content_analysis_prompt import CONTENT_ANALYSIS_PROMPT


class ContentAnalysisService:
    @inject
    def analyze_content(self, content: str, chat_model_provider: ChatModelProvider) -> ContentAnalysis:
        chat_model = chat_model_provider.get_chat_model()

        prompt = PromptTemplate.from_template(CONTENT_ANALYSIS_PROMPT)
        parser = PydanticOutputParser(pydantic_object=ContentAnalysis)

        chain = prompt | chat_model | parser

        result = chain.invoke(
            {
                "content": content,
                "format_instructions": parser.get_format_instructions()
            }
        )

        return result
