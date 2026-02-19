import sounddevice as sd
import soundfile as sf
import numpy as np


class AudioPlayer:
    def __init__(self):
        self.current_data = None
        self.current_samplerate = None

    def play(self, file_path):
        sd.stop()

        data, samplerate = sf.read(file_path, dtype="float32")

        if len(data.shape) == 1:
            data = data.reshape(-1, 1)

        self.current_data = data
        self.current_samplerate = samplerate

        sd.play(self.current_data, self.current_samplerate)

        return data

    def stop(self):
        sd.stop()
