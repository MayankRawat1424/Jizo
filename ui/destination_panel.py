import os
import json

from PySide6.QtGui import QBrush
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QFileDialog,
    QMessageBox
)
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidgetItem
import os
from PySide6.QtCore import QTimer

class DestinationPanel(QWidget):
    destination_selected = Signal(str)

    MAX_DESTINATIONS = 10

    def __init__(self, config_path):
        super().__init__()

        self.config_path = config_path

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.add_btn = QPushButton("Add Destination")
        self.remove_btn = QPushButton("Remove Selected")

        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)

        self.add_btn.clicked.connect(self.add_destination)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.list_widget.itemClicked.connect(self.emit_selected)

        self.load_destinations()

    def load_destinations(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as f:
            data = json.load(f)

        destinations = data.get("destinations", [])

        self.list_widget.clear()
        for index, path in enumerate(destinations):
            folder_name = os.path.basename(path)

            display_number = (index + 1) % 10  # 10 becomes 0
            display_text = f"{display_number}. {folder_name}"

            item = QListWidgetItem(display_text)
            item.setData(1000, path)

            self.list_widget.addItem(item)

    def save_destinations(self):
        data = {}

        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                data = json.load(f)

        data["destinations"] = [
            self.list_widget.item(i).data(1000)
            for i in range(self.list_widget.count())
        ]

        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_destination(self):
        if self.list_widget.count() >= self.MAX_DESTINATIONS:
            QMessageBox.warning(self, "Limit Reached", "Maximum 10 destinations allowed.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")

        if folder:
            # Avoid duplicates
            for i in range(self.list_widget.count()):
                if self.list_widget.item(i).text() == folder:
                    return

            folder_name = os.path.basename(folder)

            index = self.list_widget.count()
            display_number = (index + 1) % 10
            display_text = f"{display_number}. {folder_name}"

            item = QListWidgetItem(display_text)
            item.setData(1000, folder)

            self.list_widget.addItem(item)
            self.save_destinations()

    def remove_selected(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        self.list_widget.takeItem(self.list_widget.row(item))
        self.refresh_numbers()
        self.save_destinations()

    def refresh_numbers(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            path = item.data(1000)

            folder_name = os.path.basename(path)
            display_number = (i + 1) % 10
            item.setText(f"{display_number}. {folder_name}")

    def emit_selected(self, item):
        full_path = item.data(1000)
        self.destination_selected.emit(full_path)

    def flash_item(self, path, color):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.data(1000) == path:
                item.setBackground(color)

                QTimer.singleShot(400, lambda: item.setBackground(QBrush()))
                break