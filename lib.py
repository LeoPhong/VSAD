#-*- coding: utf-8 -*-

import pyaudio
import webrtcvad

import wave
class WavesRecorder(object):
    def __init__(self, FORMAT=pyaudio.paInt16, CHANNELS=1, RATE=16000, CHUNK_DURATION_MS=30):
        self.FORMAT = FORMAT
        self.CHANNELS = CHANNELS
        self.RATE = RATE
        self.CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
        #self.counter = 0
        #self.data = b''
    
    def openStream(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK_SIZE)
    
    def readStream(self):
        frame = self.stream.read(self.CHUNK_SIZE)
        #self.data += frame
        #if self.counter > 1000:
        #    record2Files('test.wav',self.data,2)
        #    print("done")
        #    import time
        #    time.sleep(5)
        #self.counter += 1
        return frame
    
    def closeStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()


class SpeechChecker(object):
    def __init__(self, rate):
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(1)
        self.rate = rate
    
    def checkSpeech(self, chunk):
        return self.vad.is_speech(chunk, self.rate)



import wave
def record2Files(path, data, sample_width):
    "Records from the microphone and outputs the resulting data to 'path'"
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(16000)
    wf.writeframes(data)
    wf.close()

def main():
    data = b''
    recorder = WavesRecorder()
    recorder.openStream()
    for _ in range(1000):
        data += recorder.readStream()
    recorder.closeStream()
    record2Files('record.wav', data, 2)
        

if __name__ == '__main__':
    main()
