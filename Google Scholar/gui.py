#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time : 2021/2/26 21:54
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QPlainTextEdit
from PySide2.QtWidgets import QMessageBox
from scholar import Scholar
import os


os.environ['QT_MAC_WANTS_LAYER'] = '1'


def handle():
    query = textEdit.toPlainText()
    s = Scholar(query, root='/Users/tangxiangong/Downloads')
    s.search()
    r = s.get_html_root()
    QMessageBox.about(window, "Result",
                      f"Successfully!\nThe html files are saved in the directory {r}.")


app = QApplication([])

window = QMainWindow()
window.resize(800, 600)
window.move(300, 310)
window.setWindowTitle("谷歌学术")

textEdit = QPlainTextEdit(window)
textEdit.setPlaceholderText("请输入关键字")
textEdit.move(45, 45)
textEdit.resize(500, 30)

button = QPushButton("搜索", window)
button.move(555, 40)
button.resize(80, 40)
button.clicked.connect(handle)

window.show()

app.exec_()

