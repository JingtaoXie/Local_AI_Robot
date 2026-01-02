import sounddevice as sd  ##voice recognizer package
import vosk ##voice recognizer model
import pyttsx3 ##from text to voice
import queue
import json

model_path="vosk-model-small-cn-0.22"

# q = queue.Queue()
duration = 5
sample_rate = 16000   ##normally 16000 Hz, should align with the sample rate for model training
sd.default.samplerate = sample_rate
sd.default.channels = 1

def startListening():
    clientCommand = sd.rec(int(duration * sample_rate), dtype='int16')
    sd.wait()
    clientCommandInBytes = clientCommand.flatten().tobytes()
    return clientCommandInBytes

def identfyingCommand(clientCommand):
    languageModel = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(languageModel, sample_rate)
    rec.AcceptWaveform(clientCommand)
    result = json.loads(rec.Result())
    return result.get("text", "")

def readingAnswer(clientCommandinText):
    engine = pyttsx3.init()
    engine.setProperty('rate', 200)  # speaking rate
    engine.setProperty('volume', 1.0)  # volume
    engine.say(clientCommandinText)
    engine.runAndWait()  # playing text

# def startSpeaking(clientCommandinText):
#     sd.play(clientCommandinText)


## Testing Command

# clientCommand = startListening()
# clientCommandinText = identfyingCommand(clientCommand)
# print(clientCommandinText)
# readingAnswer(clientCommandinText)






