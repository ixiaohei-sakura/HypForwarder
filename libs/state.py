class SingleState:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class ThreadState:
    WAIT_FOR_START = SingleState("WAIT_FOR_START")
    RUNNING = SingleState("RUNNING")
    STOPPED = SingleState("STOPPED")
    TERMINATING = SingleState("TERMINATING")


class SocketState:
    WAIT_FOR_CLIENT = SingleState("WAIT_FOR_CLIENT")
    CREATING_HANDLER_THREAD = SingleState("CREATING_HANDLER_THREAD")
    CONNECTED = SingleState("CONNECTED")
    DISCONNECTED = SingleState("DISCONNECTED")
    CLOSED = SingleState("CLOSED")
