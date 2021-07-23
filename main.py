import socket

from Config import Config
from libs.IOThread import ClientIOThread
from libs.logger import Logger
from libs.threadManager import ThreadManager


class Main:
    def __init__(self):
        self.logger = Logger("Redirector")
        self.parentSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.threadManager = ThreadManager(self.logger)

    def initParentIOStream(self):
        try:
            self.parentSocket.bind((Config.LocalProperties.host, Config.LocalProperties.port))
            self.parentSocket.listen(5)
        except OSError as e:
            self.logger.error(e)
            self.logger.error(f"Can' t Bind Address - {Config.LocalProperties.host}:{Config.LocalProperties.port}")
            self.logger.error("Please Check if there is any process using this port.")
            raise SystemExit
        else:
            self.logger.info(f"Initialized Parent IO Stream, "
                             f"Bound Addr - {Config.LocalProperties.host}:{Config.LocalProperties.port}")

    def main(self):
        self.initParentIOStream()
        self.threadManager.start()
        self.logger.info("Waiting for clientSocket connection")
        while True:
            try:
                clientSocket, address = self.parentSocket.accept()
            except KeyboardInterrupt:
                self.logger.info("Terminating All Threads...")
                self.threadManager.stopAll()
                self.threadManager.join()
                break
            else:
                self.threadManager.addThread(ClientIOThread(clientSocket, Config.TargetProperties.host,
                                                            Config.TargetProperties.port, self.logger))
        self.logger.info("Closing Parent Socket...")
        self.parentSocket.close()
        self.logger.info("Exit.")


if __name__ == '__main__':
    print("Initializing Stream Forwarder...")
    mainClass = Main()
    mainClass.main()
