Jizo is a keyboard-driven sample preview and organizing tool built for fast drum sample curation and dataset preparation.
This utility was designed to support manual dataset creation for audio classification projects by making sample sorting fast, visual, and frictionless.
(WAV-only workflow recommended)


**##Features**

**Instant Preview** : Low-latency WAV playback (sounddevice)
**Visual Analysis** : Waveform display, Spectrogram display
**Directory Browser** : Inspired by DAWs
**Destination Playlists** : 10 saved destination folders


**##Keyboard Workflow**

**Key** :	Action
**↑ / ↓** :	Navigate samples
**Space** :	Preview / Expand folder
**1–9 / 0** :	Copy to destination
**Z**	: Undo (up to 20 levels)


**##Visual Feedback**

🟢 Green : Successful copy/move
🔴 Red : Duplicate detected (skipped) Prevents duplication of samples in folders
🟡 Yellow : Undo


**##Requirements**

Python 3.10+
PySide6
sounddevice
soundfile
numpy
pyqtgraph

**Install dependencies** : pip install PySide6 sounddevice soundfile numpy pyqtgraph


