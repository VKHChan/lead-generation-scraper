from configuration import Settings
from core.chat_model import ChatModelProvider
from core.domain import ContentAnalysis
from core.storage import Storage
from core.utils import StandardFileNaming
from injector import inject
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from .content_analysis_prompt import CONTENT_ANALYSIS_PROMPT


class ContentAnalysisService:
    @inject
    def __init__(self, settings: Settings, storage: Storage):
        self._content_analysis_path = f"{settings.content_analysis_path}"
        self._storage = storage
        self._file_naming = StandardFileNaming()

    def analyze_content(self, url: str, content: str, chat_model_provider: ChatModelProvider, file_path: str) -> ContentAnalysis:
        chat_model = chat_model_provider.get_chat_model()

        prompt = PromptTemplate.from_template(CONTENT_ANALYSIS_PROMPT)
        parser = PydanticOutputParser(pydantic_object=ContentAnalysis)

        chain = prompt | chat_model | parser

        try:

            result = chain.invoke(
                {
                    "content": content,
                    "format_instructions": parser.get_format_instructions()
                }
            )

            result_dict = result.model_dump()
        except Exception as e:
            print(f"Error analyzing content: {e}")
            return None

        file_name = f"{self._content_analysis_path}/{self._file_naming.clean_url_for_file(url)}_content_analysis.json"
        if file_path:
            file_name = f"{file_path}/{file_name}"

        self._storage.write_json(file_name, result_dict)

        return result_dict
