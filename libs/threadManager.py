from threading import Thread, RLock

import time
from libs.state import ThreadState


class ThreadManager(Thread):
    def __init__(self, logger):
        super(ThreadManager, self).__init__()
        self.logger = logger
        self.name = "Thread Manager"
        self.state = ThreadState.WAIT_FOR_START
        self.threadList = []
        self.removingTmp = []
        self.lock = RLock()

    def addThread(self, thr):
        with self.lock:
            thr.name = thr.name.format(len(self.threadList))
            thr.start()
            self.threadList.append(thr)

    def stopThread(self, thr):
        thr.stop()
        thr.join()
        self.removingTmp.append(thr)

    def stopAll(self):
        with self.lock:
            for t in self.threadList:
                self.stopThread(t)
        self.stop()

    def stop(self):
        self.logger.info("Stopping...")
        self.state = ThreadState.TERMINATING

    def run(self) -> None:
        self.state = ThreadState.RUNNING
        self.logger.info("Thread Manager Started")
        while self.state != ThreadState.TERMINATING:
            with self.lock:
                try:
                    for t in self.threadList:
                        if t.threadState == ThreadState.STOPPED:
                            self.removingTmp.append(t)
                    for t in self.removingTmp:
                        self.threadList.remove(t)
                except Exception as e:
                    pass
            time.sleep(0.1)
        self.logger.info("Thread Manager Stopped >.<")
