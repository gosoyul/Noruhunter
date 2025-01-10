from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QFormLayout, QLabel, QSpinBox, QMainWindow

from config import ConfigKeys, ConfigManager


class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('설정')
        self.setMinimumWidth(400)
        self.config = ConfigManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Form Layout for Settings Fields
        form_layout = QFormLayout()

        # Window Title
        self.window_title_input = QLineEdit(self.config.get(ConfigKeys.WINDOW_TITLE))
        self.window_title_input.textChanged.connect(self.on_window_title_changed)
        form_layout.addRow("윈도우 제목", self.window_title_input)

        # Max Scrolls in its own row
        self.max_scrolls_label = QLabel("최대 스크롤")
        self.max_scrolls_input = QSpinBox()
        self.max_scrolls_input.setValue(self.config.get(ConfigKeys.MAX_SCROLLS))
        self.max_scrolls_input.valueChanged.connect(self.on_max_scrolls_changed)
        form_layout.addRow(self.max_scrolls_label, self.max_scrolls_input)

        # Scroll Repeat in its own row
        self.scroll_repeat_label = QLabel("스크롤 반복")
        self.scroll_repeat_input = QSpinBox()
        self.scroll_repeat_input.setValue(self.config.get(ConfigKeys.SCROLL_REPEAT))
        self.scroll_repeat_input.valueChanged.connect(self.on_scroll_repeat_changed)
        form_layout.addRow(self.scroll_repeat_label, self.scroll_repeat_input)

        # 부족 공헌도 제한
        self.contrib_limit_label = QLabel("부족 공헌도 제한")
        self.contrib_limit_input = QSpinBox()
        self.contrib_limit_input.setMaximum(10000)
        self.contrib_limit_input.setSingleStep(10)
        self.contrib_limit_input.setValue(self.config.get(ConfigKeys.CONTRIB_LIMIT))
        self.contrib_limit_input.valueChanged.connect(self.on_contrib_limit_changed)
        form_layout.addRow(self.contrib_limit_label, self.contrib_limit_input)

        # 클로바 API 입력 (가로로 길게 고정 제거)
        clova_layout = QVBoxLayout()
        clova_label = QLabel("클로바 API")

        self.api_url_input = QLineEdit(self.config.get([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_API_URL]))
        self.api_url_input.setPlaceholderText("엔드포인트 URL")
        self.api_url_input.textChanged.connect(self.on_api_url_changed)
        clova_layout.addWidget(self.api_url_input)

        self.x_ocr_secret_input = QLineEdit(self.config.get([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_X_OCR_SECRET]))
        self.x_ocr_secret_input.setPlaceholderText("X_OCR_SECRET")
        self.x_ocr_secret_input.textChanged.connect(self.on_x_ocr_secret_changed)
        clova_layout.addWidget(self.x_ocr_secret_input)

        form_layout.addRow(clova_label, clova_layout)

        layout.addLayout(form_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Slot methods for UI updates and saving
    def on_window_title_changed(self):
        self.config.set(ConfigKeys.WINDOW_TITLE, self.window_title_input.text())

    def on_max_scrolls_changed(self):
        self.config.set(ConfigKeys.MAX_SCROLLS, self.max_scrolls_input.value())

    def on_scroll_repeat_changed(self):
        self.config.set(ConfigKeys.SCROLL_REPEAT, self.scroll_repeat_input.value())

    def on_contrib_limit_changed(self):
        self.config.set(ConfigKeys.CONTRIB_LIMIT, self.contrib_limit_input.value())

    def on_x_ocr_secret_changed(self):
        self.config.set([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_X_OCR_SECRET], self.x_ocr_secret_input.text())

    def on_api_url_changed(self):
        self.config.set([ConfigKeys.CLOVA_API, ConfigKeys.CLOVA_API_URL], self.api_url_input.text())
