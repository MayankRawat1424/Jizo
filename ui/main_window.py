from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PySide6.QtGui import QShortcut, QKeySequence

from ui.sidebar import Sidebar
from ui.waveform_view import WaveformView
from audio.player import AudioPlayer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.shortcuts = []

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