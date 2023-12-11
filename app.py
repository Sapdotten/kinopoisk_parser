#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QPushButton, QApplication, QFileDialog, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QFont, QColor
from task_2 import copy_dataset
from os import path
from pathlib import Path
from task_1 import make_annotation
from task_5 import FilesIterator


class Example(QMainWindow):
    dataset_dir: str = None

    def __init__(self):
        super().__init__()
        self.bad_iter = None
        self.good_iter = None
        self.initUI()

    def initUI(self):

        self.setGeometry(1000, 200, 600, 800)
        self.setStyleSheet("background-color: #303956")
        self.setWindowTitle('Dataset Manager')
        self.setWindowIcon(QIcon('src/app_icon.png'))
        if not self.dataset_dir:
            self.get_dataset_btn = self.create_button(
                'Выбрать папку с датасетом...', self.init_dataset)
            widget = QWidget()
            hbox = QHBoxLayout(widget)
            hbox.addStretch(1)
            hbox.addWidget(self.get_dataset_btn)
            hbox.addStretch(1)
            self.setCentralWidget(widget)

        self.show()

    def changeUI(self):

        next_good_button = self.create_button(
            'Следующая положительная аннотация', self.next_good_review)
        next_bad_button = self.create_button(
            'Следующая отрицательная аннотация', self.next_bad_review)
        quit_button = self.create_button(
            'Выход', QCoreApplication.instance().quit)

        annotation_button = self.create_button(
            'Создать аннотацию', self.make_annotation)

        copy_button = self.create_button(
            'Копировать датасет...', self.copy_dataset)
        widget = QWidget()
        widget.setStyleSheet("background-color: #303956;")

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
                                  background-color:#416E97;
                                  border-radius: 10px;""")
        scroll_area.verticalScrollBar().setStyleSheet(
            "background-color: #A8D0DC; border-radius: 5px;")
        shadow = QGraphicsDropShadowEffect(
            blurRadius=7, xOffset=3, yOffset=3, color=QColor("#202959"))
        scroll_area.setGraphicsEffect(shadow)
        # scroll_area.verticalScrollBar().
        scroll_area.setWidgetResizable(True)
        self.label = QLabel(scroll_area)
        self.label.setStyleSheet(
            "background-color: #416E97;padding :15px; color: #D9E7E8;")
        self.label.setFont(QFont('Consolas', 15))
        scroll_area.setWidget(self.label)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        # self.label.setGeometry(
        # 0, 0, 400, scroll_area.height())
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        hbox = QVBoxLayout()
        hbox.addWidget(next_good_button)
        hbox.addWidget(next_bad_button)

        # textbox = QVBoxLayout()
        # textbox.addWidget(scroll_area)

        vrbox = QVBoxLayout()
        vrbox.addWidget(scroll_area)
        # vrbox.addStretch()
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

    def next_good_review(self):
        if not self.good_iter:
            self.good_iter = FilesIterator(self.dataset_dir, 'good')
        try:
            file_ = next(self.good_iter)
            with open(file_, 'r', encoding='utf-8') as file:
                self.label.setText(file.read())
        except StopIteration:
            self.warning_end_of_files('good')

    def next_bad_review(self):
        if not self.bad_iter:
            self.bad_iter = FilesIterator(self.dataset_dir, 'bad')
        try:
            file_ = next(self.bad_iter)
            with open(file_, 'r', encoding='utf-8') as file:
                self.label.setText(file.read())
        except StopIteration:
            self.warning_end_of_files('bad')

    def create_button(self, text: str, func) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(func)
        button
        button.resize(button.minimumSizeHint())
        button.setStyleSheet("""
                             background-color: #E3474B;
                             color: #D9E7E8;
                             font-size: 20px;
                             padding: 10px 10px 10px 10px;
                             border-radius: 5px;
                             background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
stop: 0 #E3474B, stop: 1 #6E2734);""")
        shadow = QGraphicsDropShadowEffect(
            blurRadius=7, xOffset=3, yOffset=3, color=QColor("#31021F"))
        button.setGraphicsEffect(shadow)
        button.setFont(QFont('FreeMono, monospace', 15))
        return button

    def warning_end_of_files(self, class_):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        review_type = 'положительные'
        if class_ == 'bad':
            review_type = 'отрицательные'

        msg.setText(
            f"Мы показали вам все {review_type} рецензии")
        msg.setWindowTitle('Конец рецензий')
        msg.setStandardButtons(QMessageBox.Cancel)
        dataset_btn = msg.addButton(
            f"Начать просмотр {review_type[:-1]+'х'} рецензий заново", QMessageBox.YesRole)
        if class_ == 'good':
            self.good_iter = None
            dataset_btn.clicked.connect(self.next_good_review)
        else:
            self.bad_iter = None
            dataset_btn.clicked.connect(self.next_bad_review)
        retval = msg.exec_()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
