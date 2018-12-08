import sys
from PyQt5.QtWidgets import QApplication
from AccountBook import AccountBook


class Transportation(AccountBook):
    def __init__(self):
        super().__init__(db_file='db_trans.sqlite', title='交通费')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = Transportation()
    sys.exit(app.exec_())
