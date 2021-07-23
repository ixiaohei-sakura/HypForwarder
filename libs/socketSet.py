import socket


class SocketSet(object):
    def __init__(self, clientSocket: socket.socket, targetHost: str, targetPort: int):
        super(SocketSet, self).__init__()
        self.client = clientSocket
        self.targetHost = targetHost
        self.targetPort = targetPort
        self.target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectTarget(self):
        self.target.connect((self.targetHost, self.targetPort))
        self.target.setblocking(False)
        self.client.setblocking(False)

    def closeAll(self):
        self.client.close()
        self.target.close()
