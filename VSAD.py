#-*- coding: utf-8 -*-

from multiprocessing import Queue

from Processing import RecorderProcessing
from Processing import CheckerProcessing
from Processing import WaveWriter

def main():
    frames_queue = Queue()
    segment_queue = Queue()
    Recorder = RecorderProcessing(frames_queue)
    Recorder.start()
    checker = CheckerProcessing(frames_queue, segment_queue)
    checker.start()
    writer = WaveWriter(segment_queue)
    writer.start()
    Recorder.join()
    checker.join()
    writer.join()

if __name__ == '__main__':
    main()