#-*- coding: utf-8 -*-

import os
import time
import wave
from multiprocessing import Process
from multiprocessing import Queue


from lib import WavesRecorder
from lib import SpeechChecker


CHANNELS=1
RATE=16000
CHUNK_DURATION_MS=30
VOICE_INTERVAL=5

class RecorderProcessing(Process):
    def __init__(self, wave_frames:Queue):
        Process.__init__(self)
        self.wave_frames = wave_frames
        self.recorder = WavesRecorder(CHANNELS=CHANNELS, RATE=RATE, CHUNK_DURATION_MS=CHUNK_DURATION_MS)
    
    def run(self):
        self.recorder.openStream()

        while True:
            frames_data = self.recorder.readStream()
            timestamp = time.time()
            self.wave_frames.put((timestamp, frames_data))
    
class CheckerProcessing(Process):
    def __init__(self, wave_frames:Queue, wave_segment:Queue):
        Process.__init__(self)
        self.wave_frames = wave_frames
        self.wave_segment = wave_segment
        self.checker = SpeechChecker(RATE)
    
    def run(self):
        # wave_status表示当前音频帧的状态
        #                   0：静音状态
        #                   1：有声音
        #                   2：声音之间的小间隔
        #                   3：结束
        wave_status = 0
        segment = []
        mute_time = 0.0
        while True:
            frame = self.wave_frames.get()
            if wave_status == 0:
                if self.checker.checkSpeech(frame[1]) == True:
                    wave_status = 1
                    segment.append(frame)
                continue

            if wave_status == 1:
                if self.checker.checkSpeech(frame[1]) == True:
                    segment.append(frame)
                else:
                    segment.append(frame)
                    mute_time = frame[0]
                    wave_status = 2
                continue

            if wave_status == 2:
                if self.checker.checkSpeech(frame[1]) == True:
                    segment.append(frame)
                    mute_time = 0.0
                    wave_status = 1
                else:
                    if frame[0]-mute_time < float(VOICE_INTERVAL):
                        segment.append(frame)
                    else:
                        wave_status = 3
                continue
                    
            if wave_status == 3:
                self.wave_segment.put(segment)
                segment = []
                mute_time = 0.0
                wave_status = 0
                continue
                

class WaveWriter(Process):
    def __init__(self, wave_segment:Queue):
        Process.__init__(self)
        self.wave_segment = wave_segment
    
    def run(self):
        #建立相关目录
        wav_path = os.path.join(os.getcwd(), 'wav')
        if not os.path.isdir(wav_path):
            os.makedirs(wav_path)
        while True:
            segment = self.wave_segment.get()
            start_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(segment[0][0]))
            filename = os.path.join(wav_path, start_time+'.wav')
            wave_data = b''
            for element in segment:
                wave_data += element[1]
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setframerate(RATE)
            wf.setsampwidth(2)
            wf.writeframes(wave_data)
            wf.close()
