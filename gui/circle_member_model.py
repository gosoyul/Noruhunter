from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from circle_member import CircleMember, CircleMemberManager

# 컬럼명 매핑
COLUMN_MAP = {
    "nickname": {"label": "닉네임"},
    "uid": {"label": "UID"},
    "arcalive_id": {"label": "아카라이브 ID"},
    "join_date": {"label": "가입일"},
    "join_period": {"label": "가입기간"},  # 가입기간은 자동 계산
    "position": {"label": "직위"},  # 기본 직위
    "remark": {"label": "비고"},
}


class CircleMemberModel(QStandardItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # COLUMN_MAP을 이용해 테이블 헤더 설정
        for col_idx, (header_key, value) in enumerate(COLUMN_MAP.items()):
            header_item = QStandardItem(value["label"])
            header_item.setData(header_key, Qt.UserRole)
            self.setHorizontalHeaderItem(col_idx, header_item)

        self.load_data()
        self.itemChanged.connect(self.on_item_changed)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and self.get_column_key(index.column()) == "join_period":
            circle_member_manager = CircleMemberManager()
            return circle_member_manager.members[index.row()].join_period

        return super().data(index, role)

    def get_column_key(self, col_idx):
        return self.headerData(col_idx, Qt.Horizontal, Qt.UserRole)

    def load_data(self):
        """CircleMemberManager의 데이터를 테이블 모델로 로드"""
        self.setRowCount(0)  # 기존 데이터 초기화

        circle_member = CircleMemberManager()
        for member in circle_member.members:
            self.appendRow(self.member_to_items(member))

    def member_to_items(self, member: CircleMember):
        """CircleMember 객체를 QStandardItem 리스트로 변환"""
        return [
            QStandardItem(member.nickname),
            QStandardItem(member.uid),
            QStandardItem(member.arcalive_id),
            QStandardItem(member.join_date),
            None,
            QStandardItem(member.position),
            QStandardItem(member.remark)
        ]

    def add_member(self):
        """새로운 서클원을 모델과 매니저에 추가"""
        circle_member_manager = CircleMemberManager()
        new_member = circle_member_manager.add_member()
        circle_member_manager.save_to_json()

        self.appendRow(self.member_to_items(new_member))

    def remove_members(self, row_indices):
        """새로운 서클원을 모델과 매니저에 추가"""

        if not row_indices:
            return  # 선택된 행이 없으면 아무 작업도 하지 않음

        circle_member_manager = CircleMemberManager()
        for row_idx in sorted(row_indices, reverse=True):
            circle_member_manager.remove_member(row_idx)
            self.removeRow(row_idx)

        circle_member_manager.save_to_json()

    def on_item_changed(self, item):
        """itemChanged 시 처리할 이벤트"""
        row = item.row()
        column = item.column()

        # 수정된 데이터 가져오기
        key = list(COLUMN_MAP.keys())[column]

        # CircleMemberManager의 수정된 데이터 업데이트
        manager = CircleMemberManager()
        member = manager.members[row]

        setattr(member, key, item.text())

        # 수정된 데이터를 저장
        manager.save_to_json()
