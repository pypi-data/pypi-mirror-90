from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMessageBox

from mp3monitoring.gui import pkg_data


def question_message_box(win_title: str, msg: str):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setWindowIcon(QIcon(str(pkg_data.LOGO)))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_title)
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
    reply = msg_box.exec()
    return reply


def information_message_box(win_title: str, msg: str):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setWindowIcon(QIcon(str(pkg_data.LOGO)))

    msg_box.setText(msg)
    msg_box.setWindowTitle(win_title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()
