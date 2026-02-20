from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QShortcut, QKeySequence

from ui.sidebar import Sidebar
from ui.waveform_view import WaveformView
from audio.player import AudioPlayer
from ui.destination_panel import DestinationPanel
import os
import shutil
from PySide6.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shortcuts = []

        self.undo_stack = []
        self.MAX_UNDO = 20

        undo_shortcut = QShortcut(QKeySequence("Z"), self)
        undo_shortcut.activated.connect(self.undo_last_operation)
        self.shortcuts.append(undo_shortcut)

        for i in range(10):
            key = str(i)

            # Copy
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(lambda num=i: self.send_to_number(num, move=False))
            self.shortcuts.append(shortcut)

            # Move
            move_shortcut = QShortcut(QKeySequence(f"Ctrl+{key}"), self)
            move_shortcut.activated.connect(lambda num=i: self.send_to_number(num, move=True))
            self.shortcuts.append(move_shortcut)

        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config.json"
        )

        self.setWindowTitle("Jizo")
        self.resize(1200, 700)

        self.player = AudioPlayer()
        self.current_file = None

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()
        central.setLayout(layout)

        # Sidebar
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar, 1)

        # Destination Panel
        self.destination_panel = DestinationPanel(self.config_path)
        layout.addWidget(self.destination_panel, 1)

        self.current_destination = None
        self.destination_panel.destination_selected.connect(
            self.set_current_destination
        )

        # Waveform + Spectrogram
        self.waveform_view = WaveformView()
        layout.addWidget(self.waveform_view, 3)

        # Connect sidebar signal
        self.sidebar.file_selected.connect(self.handle_file_selected)

        # Shortcuts
        self.shortcut_map = {
            "Ctrl+1": r"D:\Samples\Kicks",
            "Ctrl+2": r"D:\Samples\Snares",
        }

        for key, destination in self.shortcut_map.items():
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(
                lambda dest=destination: self.copy_to_destination(dest)
            )
            self.shortcuts.append(shortcut)

    def handle_file_selected(self, file_path):
        self.current_file = file_path

        audio_data = self.player.play(file_path)
        self.waveform_view.update_waveform(audio_data)
        self.waveform_view.update_spectrogram(
            audio_data,
            self.player.current_samplerate
        )

    def set_current_destination(self, path):
        self.current_destination = path

    def copy_to_selected_destination(self, move=False):
        if not self.current_file or not self.current_destination:
            return

        if not os.path.exists(self.current_destination):
            os.makedirs(self.current_destination)

        filename = os.path.basename(self.current_file)
        target_path = os.path.join(self.current_destination, filename)

        # Duplicate check
        if os.path.exists(target_path):
            self.destination_panel.flash_item(
                self.current_destination,
                QColor("#aa3333")  # red
            )
            return

        try:
            if move:
                shutil.move(self.current_file, target_path)
            else:
                shutil.copy2(self.current_file, target_path)

            # Save for undo
            # Push to undo stack
            self.undo_stack.append((
                self.current_file,
                target_path,
                move
            ))

            # Limit stack size
            if len(self.undo_stack) > self.MAX_UNDO:
                self.undo_stack.pop(0)

            self.destination_panel.flash_item(
                self.current_destination,
                QColor("#33aa33")  # green
            )

        except Exception as e:
            print("Operation failed:", e)

    def send_to_number(self, number, move=False):
        if not self.current_file:
            return

        index = number - 1 if number != 0 else 9

        if index < 0:
            return

        if index >= self.destination_panel.list_widget.count():
            return

        item = self.destination_panel.list_widget.item(index)
        destination = item.data(1000)

        self.current_destination = destination
        self.copy_to_selected_destination(move=move)

    def undo_last_operation(self):
        if not self.undo_stack:
            return

        original_path, target_path, was_move = self.undo_stack.pop()

        if not os.path.exists(target_path):
            return

        try:
            if was_move:
                shutil.move(target_path, original_path)
            else:
                os.remove(target_path)

            self.destination_panel.flash_item(
                os.path.dirname(target_path),
                QColor("#cccc33")  # yellow
            )

        except Exception as e:
            print("Undo failed:", e)