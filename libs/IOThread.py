import select
from threading import Thread

from Config import Config
from libs.dataSet import DataSet
from libs.logger import Logger
from libs.socketSet import SocketSet
from libs.state import SocketState, ThreadState


class ClientIOThread(Thread):
    def __init__(self, clientSocket, targetHost, targetPort, logger: Logger):
        super(ClientIOThread, self).__init__()
        self.logger = logger
        self.name = "Client IO Thread - #{}"
        self.daemon = True
        self.threadState = ThreadState.WAIT_FOR_START
        self.socketState = SocketState.CONNECTED
        self.socketSet = SocketSet(clientSocket, targetHost, targetPort)
        self.dataSet = DataSet()

    def initSocket(self):
        self.logger.info("Initializing IO streams")
        self.socketSet.connectTarget()

    def start(self) -> None:
        self.logger.info(f"Starting {self.name}")
        super(ClientIOThread, self).start()

    def stop(self):
        self.threadState = ThreadState.TERMINATING
        self.socketState = SocketState.DISCONNECTED

    def run(self):
        self.threadState = ThreadState.RUNNING
        try:
            self.initSocket()
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Target Host Error, Thread Stopped.")
            self.threadState = ThreadState.TERMINATING
        else:
            self.logger.info(f"Client Thread started, Target Host Connected. "
                             f"Host name: {self.socketSet.targetHost}:{self.socketSet.targetPort}")
        while self.threadState != ThreadState.TERMINATING and self.socketState != SocketState.DISCONNECTED:
            inputs = [self.socketSet.client, self.socketSet.target]
            outputs = []

            if len(self.dataSet.dataToClient) > 0:
                outputs.append(self.socketSet.client)

            if len(self.dataSet.dataToHost) > 0:
                outputs.append(self.socketSet.target)

            try:
                inputsReady, outputsReady, errorsReady = select.select(inputs, outputs, [], 1.0)
            except Exception as e:
                self.threadState = ThreadState.TERMINATING
                self.logger.error(e)
                self.logger.error("Error when selecting IO stream. Thread stopped.")
            else:
                for inp in inputsReady:
                    if inp == self.socketSet.client:
                        try:
                            data = self.socketSet.client.recv(Config.SocketProperties.MAX_BUFF_SIZE)
                        except Exception as e:
                            self.logger.error(e)
                            self.logger.error("Error while receiving data from clientSocket. Thread stopped.")
                        else:
                            if data is not None:
                                if len(data) > 0:
                                    self.dataSet.dataToHost += data
                                else:
                                    self.socketState = SocketState.DISCONNECTED
                    elif inp == self.socketSet.target:
                        try:
                            data = self.socketSet.target.recv(Config.SocketProperties.MAX_BUFF_SIZE)
                        except Exception as e:
                            self.logger.error(e)
                            self.logger.error("Error while receiving data from target. Thread stopped.")
                        else:
                            if data is not None:
                                if len(data) > 0:
                                    self.dataSet.dataToClient += data
                                else:
                                    self.socketState = SocketState.DISCONNECTED
                for out in outputsReady:
                    if self.socketState != SocketState.DISCONNECTED:
                        if out == self.socketSet.client and len(self.dataSet.dataToClient) > 0:
                            bytesWritten = self.socketSet.client.send(self.dataSet.dataToClient)
                            self.logger.info(f"Client \033[1;34m<===\033[0m Target "
                                             f"[RawLength = {len(self.dataSet.dataToClient)}] "
                                             f"[SentLength = {bytesWritten}] "
                                             f"[RestLength = {len(self.dataSet.dataToClient) - bytesWritten}]")
                            if bytesWritten > 0:
                                self.dataSet.dataToClient = self.dataSet.dataToClient[bytesWritten:]
                        elif out == self.socketSet.target and len(self.dataSet.dataToHost) > 0:
                            bytesWritten = self.socketSet.target.send(self.dataSet.dataToHost)
                            self.logger.info(f"Client \033[1;33m===>\033[0m Target "
                                             f"[RawLength = {len(self.dataSet.dataToHost)}] "
                                             f"[SentLength = {bytesWritten}] "
                                             f"[RestLength = {len(self.dataSet.dataToHost) - bytesWritten}]")
                            if bytesWritten > 0:
                                self.dataSet.dataToHost = self.dataSet.dataToHost[bytesWritten:]
        self.logger.info("Stopping Thread...")
        self.logger.info("Closing IO Streams...")
        self.socketState = SocketState.CLOSED
        self.socketSet.closeAll()
        self.logger.info("Terminated.")
