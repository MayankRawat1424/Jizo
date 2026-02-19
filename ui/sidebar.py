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
from PySide6.QtCore import Qt, Signal


class Sidebar(QWidget):
    file_selected = Signal(str)  # Emit file path when WAV clicked

    def __init__(self):
        super().__init__()

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
