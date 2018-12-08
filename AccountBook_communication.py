import sys
from PyQt5.QtWidgets import QApplication
from AccountBook import AccountBook


class Communication(AccountBook):
    def __init__(self):
        super().__init__(db_file='db_communication.sqlite')
        self.ui.ltitle_label.setText("百联置业报销登记系统 - 通讯费       ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Communication()
    sys.exit(app.exec_())
