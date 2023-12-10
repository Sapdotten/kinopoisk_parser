#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QFileDialog, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from task_2 import copy_dataset
from os import path
from pathlib import Path
from task_1 import make_annotation


class Example(QMainWindow):
    dataset_dir: str = None

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 200, 600, 800)
        self.setWindowTitle('Dataset Manager')
        self.setWindowIcon(QIcon('src/app_icon.png'))
        if not self.dataset_dir:
            self.get_dataset_btn = QPushButton('Выбрать папку с датасетом...')
            self.get_dataset_btn.resize(self.get_dataset_btn.sizeHint())
            self.get_dataset_btn.clicked.connect(self.init_dataset)
            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.addStretch(1)
            hbox.addWidget(self.get_dataset_btn)
            hbox.addStretch(1)
            self.setCentralWidget(widget)

        self.show()

    def changeUI(self):
        next_button = QPushButton('Следующий отзыв')
        previous_button = QPushButton('Предыдщий отзыв')
        quit_button = QPushButton('Выход')
        quit_button.clicked.connect(QCoreApplication.instance().quit)
        quit_button.resize(quit_button.sizeHint())

        annotation_button = QPushButton('Создать аннотацию')
        annotation_button.clicked.connect(self.make_annotation)
        annotation_button.resize(annotation_button.sizeHint())

        copy_button = QPushButton('Копировать датасет...')
        copy_button.clicked.connect(self.copy_dataset)
        copy_button.resize(copy_button.sizeHint())

        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Quit button')
        widget = QWidget()
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setGeometry(200, 150, 100, 50)
        with open('dataset\\good\\0001.txt', encoding='utf-8') as f:
            self.label.setText(f.read())

        hbox = QHBoxLayout()
        hbox.addWidget(previous_button)
        hbox.addWidget(next_button)

        textbox = QHBoxLayout()
        textbox.addWidget(self.label)

        vrbox = QVBoxLayout()
        vrbox.addLayout(textbox)
        vrbox.addStretch(1)
        vrbox.addLayout(hbox)

        btnvbox = QVBoxLayout()
        btnvbox.addWidget(annotation_button)
        btnvbox.addWidget(copy_button)
        btnvbox.addWidget(quit_button)
        btnvbox.addStretch(1)

        finbox = QHBoxLayout(widget)
        finbox.addLayout(btnvbox)
        finbox.addLayout(vrbox)
        self.setGeometry(300, 300, 800, 600)
        self.setCentralWidget(widget)

        self.show()

    def init_dataset(self):
        self.dataset_dir = QFileDialog.getExistingDirectory(
            self, 'Выберите папку, в которой лежит датасет')
        self.dataset_dir = path.join(*(self.dataset_dir.split('/')))
        self.dataset_dir = self.dataset_dir.replace("C:", "C:\\")
        if len(self.dataset_dir) != 0 and self.dataset_exists():
            self.changeUI()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(
                "Мы не можем найти датасет по указанному пути, попробуйте указать новый.")
            msg.setWindowTitle('Неверный путь')
            msg.setStandardButtons(QMessageBox.Cancel)
            dataset_btn = msg.addButton(
                "Указать новый путь", QMessageBox.YesRole)
            dataset_btn.clicked.connect(self.init_dataset)
            retval = msg.exec_()

    def copy_dataset(self):
        if not self.dataset_dir:
            self.get_dataset()
        new_dir = QFileDialog.getExistingDirectory(
            self, 'Выберите папку, в которую необходимо скопировать датасет')
        new_dir = path.join(*(new_dir.split('/')))
        new_dir = new_dir.replace("C:", "C:\\")
        copy_dataset(self.dataset_dir, new_dir)

    def dataset_exists(self) -> bool:
        if not path.exists(path.join(self.dataset_dir, 'bad')) or not path.exists(path.join(self.dataset_dir, 'good')):
            return False
        return True

    def make_annotation(self):
        annotation_file = QFileDialog.getSaveFileName(
            None, "Save file", ".", "CSV Files (*.csv)")
        if annotation_file[0]:
            make_annotation(annotation_file[0], self.dataset_dir)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
