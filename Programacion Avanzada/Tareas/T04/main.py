from PyQt5.QtWidgets import QApplication
from client.game.frontend import pregame_windows
import sys


def hook(type, value, traceback):
    print(type)
    print(traceback)

if __name__ == "__main__":
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    window = pregame_windows.FirstWindow()
    window.show()
    sys.exit(app.exec())
