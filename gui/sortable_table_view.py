from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTableView


class SortableTableView(QTableView):
    def __init__(self, source_model: QStandardItemModel):
        super().__init__()

        self.source_model = source_model

        # Proxy Model 생성 및 설정
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(source_model)
        self.setModel(self.proxy_model)

        # 정렬 관련 변수
        self.sorted_column = None  # 현재 정렬된 열
        self.sort_order = Qt.AscendingOrder  # 정렬 방향

        # 처음에는 정렬 비활성화 (중요!)
        self.setSortingEnabled(False)

        # 헤더 클릭 이벤트 연결
        self.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

    def on_header_clicked(self, column):
        """ 헤더 클릭 시 정렬을 토글하거나 원본 상태로 복구 """
        if self.sorted_column == column:
            if self.sort_order == Qt.AscendingOrder:
                self.sort_order = Qt.DescendingOrder
            elif self.sort_order == Qt.DescendingOrder:
                self.clear_sorting()  # 정렬 해제 (원본 순서로 복구)
                return
        else:
            self.sorted_column = column
            self.sort_order = Qt.AscendingOrder

        # 정렬 수행 (헤더 클릭 시만 활성화)
        self.setModel(self.proxy_model)  # ProxyModel 적용
        self.setSortingEnabled(True)
        self.proxy_model.sort(column, self.sort_order)

    def clear_sorting(self):
        """ 정렬 해제 후 다시 정렬할 수 있도록 프록시 모델을 재적용 """
        self.sorted_column = None
        self.sort_order = Qt.AscendingOrder

        # 정렬 해제
        self.setSortingEnabled(False)  # 정렬 기능 비활성화
        self.setModel(self.source_model)  # 원본 모델로 복원

    def get_selected_model_indices(self):
        row_indices = []
        for index in self.selectedIndexes():
            if self.isSortingEnabled():
                row_index = self.proxy_model.mapToSource(index)
            else:
                row_index = self.source_model.index(index.row(), index.column())

            row_indices.append(row_index.row())

        return row_indices