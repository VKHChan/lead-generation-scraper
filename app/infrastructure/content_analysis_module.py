from core.content_analysis import ContentAnalysisService
from injector import Binder, Module


class ContentAnalysisModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(ContentAnalysisService, to=ContentAnalysisService)
