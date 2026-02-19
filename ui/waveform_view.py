import pyqtgraph as pg
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt


class WaveformView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.splitter = QSplitter(Qt.Vertical)
        layout.addWidget(self.splitter)

        # ---- Waveform Plot ----
        self.waveform_plot = pg.PlotWidget()
        self.waveform_plot.setBackground("#1e1e1e")
        self.waveform_plot.setMenuEnabled(False)
        self.waveform_plot.setMouseEnabled(x=False, y=False)
        self.waveform_plot.showGrid(x=False, y=False)

        self.waveform_curve = self.waveform_plot.plot(pen=pg.mkPen("#00ff88"))

        self.splitter.addWidget(self.waveform_plot)

        # ---- Spectrogram Plot ----
        self.spectrogram_plot = pg.PlotWidget()
        self.spectrogram_plot.setBackground("#1e1e1e")
        self.spectrogram_plot.setMenuEnabled(False)
        self.spectrogram_plot.setMouseEnabled(x=False, y=False)

        self.spectrogram_img = pg.ImageItem()
        self.spectrogram_plot.addItem(self.spectrogram_img)

        self.splitter.addWidget(self.spectrogram_plot)

        self.splitter.setSizes([400, 300])

    def update_waveform(self, audio_data):
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]

        # Downsample waveform
        max_points = 5000
        if len(audio_data) > max_points:
            factor = len(audio_data) // max_points
            audio_data = audio_data[::factor]

        self.waveform_plot.clear()
        self.waveform_curve = self.waveform_plot.plot(audio_data, pen=pg.mkPen("#00ff88"))
        self.waveform_plot.setYRange(-1, 1)
        self.waveform_plot.showAxis("left")
        self.waveform_plot.showAxis("bottom")

    def update_spectrogram(self, audio_data, samplerate):
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]

        n_fft = 1024
        hop = 256

        window = np.hanning(n_fft)
        frames = []

        for i in range(0, len(audio_data) - n_fft, hop):
            frame = audio_data[i:i + n_fft] * window
            spectrum = np.fft.rfft(frame)
            frames.append(np.abs(spectrum))

        if not frames:
            return

        spec = np.array(frames).T

        # Convert to dB scale
        spec = 20 * np.log10(spec + 1e-10)

        # Normalize
        spec -= spec.min()
        spec /= spec.max()

        # Flip so low frequencies at bottom
        spec = np.flipud(spec)

        # Set image
        self.spectrogram_img.setImage(spec, autoLevels=False)
        self.spectrogram_img.setLookupTable(
            pg.colormap.get("inferno").getLookupTable()
        )
        self.spectrogram_img.setLevels([0, 1])



