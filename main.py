import queue
import sounddevice as sd
import vosk
import base_skills
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()

model = vosk.Model("small-ru")

device = sd.default.device = 0, 4
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def main():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0], dtype='int16', channels=1,
                           callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())


if __name__ == "__main__":
    main()
