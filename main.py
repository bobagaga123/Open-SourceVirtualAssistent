import queue
import sounddevice as sd
import vosk
from skills import import_all_py_files, execute_skill
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

q = queue.Queue()

model = vosk.Model("small-ru")
skills_counter, skill_names = import_all_py_files(directory="skills")
device = sd.default.device = 0, 4
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    q.put(bytes(indata))

def recognize(data, vectorizer, clf):
    base_skills_NAME = execute_skill("base_skills", "NAME")
    called = base_skills_NAME.intersection(data.split())
    if not called:
        return
    data.replace(list(called)[0], '')
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    cathegory = answer.split()[0]
    funcname = answer.split()[1]
    print(" ".join(answer.split()[2:]))
    print(execute_skill(cathegory, funcname))

def main():
    dataset = {}
    for i in range(skills_counter):
        dataset_from_current_skill = execute_skill(skill_names[i],"data_set")
        dataset.update(dataset_from_current_skill)

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(dataset.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(dataset.values()))

    del dataset

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
