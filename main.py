import queue
import sounddevice as sd
import vosk
from skills import base_skills
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
q = queue.Queue()

model = vosk.Model("small-ru")

device = sd.default.device = 0, 4
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    called = base_skills.NAME.intersection(data.split())
    if not called:
        return
    data.replace(list(called)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    print(answer)

def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(base_skills.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(base_skills.data_set.values()))

    del base_skills.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0], dtype='int16', channels=1,
                           callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)

if __name__ == "__main__":
    main()
