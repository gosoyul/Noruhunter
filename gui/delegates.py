from datetime import datetime

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import (
    QDateEdit, QComboBox, QStyledItemDelegate
)


class DateEditDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self, parent, option, index):
        # 날짜 선택기를 위한 QDateEdit 생성
        editor = QDateEdit(parent)
        editor.setCalendarPopup(True)  # 캘린더 팝업 활성화
        editor.setDisplayFormat('yyyy-MM-dd')  # 날짜 형식 설정
        return editor

    def setEditorData(self, editor, index):
        # 셀 데이터 값을 날짜 편집기로 설정
        value = index.model().data(index, Qt.EditRole)
        if value:
            # 유효한 날짜 형식이 아니라면 오늘 날짜를 기본값으로 설정
            date = QDate.fromString(value, 'yyyy-MM-dd')
            if date.isValid():
                editor.setDate(date)
            else:
                editor.setDate(QDate.currentDate())  # 날짜 형식이 잘못된 경우 오늘 날짜
        else:
            editor.setDate(QDate.currentDate())  # 값이 없으면 오늘 날짜 설정

    def setModelData(self, editor, model, index):
        # 날짜 선택기로 변경된 값을 모델에 반영
        model.setData(index, editor.date().toString('yyyy-MM-dd'), Qt.EditRole)


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, item_list):
        super().__init__()
        self.item_list = item_list

    def createEditor(self, parent, option, index):
        # 콤보박스 생성
        editor = QComboBox(parent)
        for item in self.item_list:
            editor.addItem(item)
        return editor

    def setEditorData(self, editor, index):
        # 셀 데이터 값으로 콤보박스를 설정
        value = index.model().data(index, Qt.EditRole)
        if value:
            index = editor.findText(value)
            if index != -1:
                editor.setCurrentIndex(index)

    def setModelData(self, editor, model, index):
        # 콤보박스에서 선택된 값을 모델에 반영
        model.setData(index, editor.currentText(), Qt.EditRole)


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None  # 편집기 생성 안 함 (즉, 편집 불가)


class ReadOnlyAndFormatDelegate(QStyledItemDelegate):
    def __init__(self, prefix="", postfix="", parent=None):
        super().__init__(parent)
        self.prefix = prefix
        self.postfix = postfix

    def displayText(self, text, locale):
        return f"{self.prefix}{text}{self.postfix}"

    def createEditor(self, parent, option, index):
        return None  # 편집 불가능하게 처리