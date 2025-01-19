import sys

from PyQt5.QtWidgets import QApplication

from circle_member import CircleMemberManager
from config import ConfigManager
from gui import MainWindow


if __name__ == "__main__":
    # 사용자 설정 로드
    config = ConfigManager()
    circle_member_manager = CircleMemberManager()

    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
