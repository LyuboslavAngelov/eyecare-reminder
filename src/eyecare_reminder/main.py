import sys

from PyQt5.QtWidgets import QApplication

from . import eyecare_reminder, view


def main():
    _app = QApplication(sys.argv)
    _app.setQuitOnLastWindowClosed(False)
    _eyecare = eyecare_reminder.EyecareReminder()
    _view = view.View(_eyecare)
    _eyecare.setup(_view)
    _view.show()
    _app.exec()


if __name__ == "__main__":
    main()
