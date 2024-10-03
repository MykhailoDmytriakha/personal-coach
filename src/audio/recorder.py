import sounddevice as sd
import soundfile as sf
import queue
import threading
import datetime
import os

class AudioRecorder:
    def __init__(self, recordings_folder):
        self.recordings_folder = recordings_folder
        self.is_recording = False
        self.audio_queue = queue.Queue()
    
    def start_recording(self):
        self.is_recording = True
        self.audio_queue = queue.Queue()
        threading.Thread(target=self._record_thread, daemon=True).start()
    
    def stop_recording(self):
        self.is_recording = False
        return self.file_path
    
    def _record_thread(self):
        self.file_path = self._generate_filename()
        with sf.SoundFile(self.file_path, mode='w', samplerate=44100, channels=1, subtype='PCM_16') as file:
            with sd.InputStream(samplerate=44100, channels=1, callback=self._audio_callback):
                while self.is_recording:
                    file.write(self.audio_queue.get())
    
    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())
    
    def _generate_filename(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        return os.path.join(self.recordings_folder, f"{timestamp}-recording.wav")