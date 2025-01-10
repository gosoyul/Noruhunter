from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QHeaderView, QAction
)

from config import ConfigManager
from extractors import CircleMemberExtractor, DustFrontlineExtractor
from gui.circle_member_model import CircleMemberModel, COLUMN_MAP
from gui.config_window import ConfigWindow
from gui.delegates import ComboBoxDelegate, DateEditDelegate, ReadOnlyAndFormatDelegate
from gui.sortable_table_view import SortableTableView

# 직위 리스트
POSITIONS = ["서클장", "부서클장", "서클원"]

circle_member_extractor = CircleMemberExtractor()
dust_frontline_extractor = DustFrontlineExtractor()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.config_window = ConfigWindow()

        self.setWindowTitle("Noruhunter")
        self.resize(900, 600)  # 창 크기 조정

        # 레이아웃 초기화
        self._init_layout()

    def _init_layout(self):
        """레이아웃 초기화"""

        # 메뉴바 설정
        menu_bar = self.menuBar()

        # 추출 메뉴 생성
        extract_menu = menu_bar.addMenu("인게임 목록 추출")

        # 서클원 추출 액션 추가
        circle_action = QAction("서클원 추출", self)
        circle_action.triggered.connect(lambda: circle_member_extractor.extract(self))
        extract_menu.addAction(circle_action)

        # 흙먼지전선 추출 액션 추가
        dust_action = QAction("흙먼지전선 추출", self)
        dust_action.triggered.connect(dust_frontline_extractor.extract)
        extract_menu.addAction(dust_action)

        # "설정" 메뉴 항목을 바로 추가
        config_action = QAction("설정", self)
        config_action.triggered.connect(self.on_config_click)
        menu_bar.addAction(config_action)

        # 모델 초기화
        self.model = CircleMemberModel()

        # 테이블 초기화
        self.circle_member_table = self._init_circle_member_table()

        self.add_button = QPushButton("서클원 추가", self)
        self.add_button.clicked.connect(self.model.add_member)

        self.remove_button = QPushButton("서클원 삭제", self)
        self.remove_button.clicked.connect(self.remove_members)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)

        # 메인 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.circle_member_table)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _init_circle_member_table(self):
        table = SortableTableView(self.model)

        # 최소 크기 설정 (예: 100px로 설정)
        table.horizontalHeader().setMinimumSectionSize(100)

        # 마지막 '비고' 컬럼만 Stretch로 설정
        table.horizontalHeader().setSectionResizeMode(len(COLUMN_MAP) - 1, QHeaderView.Stretch)

        # delegate 지정
        self.delegates = {
            "position": ComboBoxDelegate(POSITIONS),
            "join_date": DateEditDelegate(),
            "join_period": ReadOnlyAndFormatDelegate(postfix="일"),
        }

        # 열 이름을 기준으로 날짜 선택기 적용
        for col in range(self.model.columnCount()):
            header_key = self.model.headerData(col, Qt.Horizontal, Qt.UserRole)
            delegate = self.delegates.get(header_key)
            if delegate:
                table.setItemDelegateForColumn(col, delegate)

        return table

    def on_config_click(self):
        self.config_window.setWindowModality(2)
        self.config_window.show()

    def remove_members(self):
        """ 선택한 서클원 삭제 """
        row_indices = self.circle_member_table.get_selected_model_indices()
        self.model.remove_members(row_indices)
