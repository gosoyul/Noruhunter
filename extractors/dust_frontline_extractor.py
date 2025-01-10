from utils import window
from . import Extractor


class DustFrontlineExtractor(Extractor):
    def __init__(self):
        super().__init__(None, None)

    def get_dynamic_ratio(self, hwnd=None):
        pass

    def extract(self):
        window.show_message("추출", "다음 이벤트 때 개발 예정")

    def before_export(self, hwnd=None):
        pass

    def after_export(self, hwnd=None):
        pass

    def extracted_text_to_excel_data(self, extracted_text):
        pass
