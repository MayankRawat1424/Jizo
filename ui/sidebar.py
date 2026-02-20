from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QTreeView,
    QFileDialog,
    QFileSystemModel,
    QHeaderView,
    QSizePolicy
)
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import Qt, Signal, QTimer

import json
import os

class Sidebar(QWidget):
    file_selected = Signal(str)  # Emit file path when WAV clicked

    def __init__(self):
        super().__init__()
        self.config_path = os.path.join(os.getcwd(), "config.json")
        self.load_last_directory()

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Root selection button
        self.choose_btn = QPushButton("Set Root Directory")
        self.choose_btn.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_btn)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath("")

        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        # Hide extra columns
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        header = self.tree.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tree.setHorizontalScrollMode(QTreeView.ScrollPerPixel)
        self.tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(self.tree, 1)

        self.tree.clicked.connect(self.handle_click)
        # Spacebar shortcut for preview / expand
        self.space_shortcut = QShortcut(QKeySequence("Space"), self.tree)
        self.space_shortcut.activated.connect(self.handle_space)
        QTimer.singleShot(0, self.load_last_directory)

    def handle_click(self, index):
        file_path = self.model.filePath(index)

        if self.model.isDir(index):
            if self.tree.isExpanded(index):
                self.tree.collapse(index)
            else:
                self.tree.expand(index)
        else:
            if file_path.lower().endswith(".wav"):
                self.file_selected.emit(file_path)

    def choose_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Root Folder")

        if folder:
            index = self.model.index(folder)
            self.tree.setRootIndex(index)
            self.save_last_directory(folder)

    def save_last_directory(self, folder):
        data = {
            "last_root_directory": folder
        }

        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)

    def load_last_directory(self):
        if not os.path.exists(self.config_path):
            return

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)

            folder = data.get("last_root_directory")

            if folder and os.path.exists(folder):
                index = self.model.index(folder)
                self.tree.setRootIndex(index)

        except Exception:
            pass

    def handle_space(self):
        index = self.tree.currentIndex()

        if not index.isValid():
            return

        file_path = self.model.filePath(index)

        if self.model.isDir(index):
            if self.tree.isExpanded(index):
                self.tree.collapse(index)
            else:
                self.tree.expand(index)
        else:
            if file_path.lower().endswith(".wav"):
                self.file_selected.emit(file_path)