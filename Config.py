class Config:
    class LocalProperties:
        HOST = "0.0.0.0"
        PORT = 25565

    class TargetProperties:
        # HOST = "mc.hypixel.net"  # 等效于下面的
        # HOST = "172.65.230.98"  # 等效与上面的
        HOST = "127.0.0.1"
        PORT = 25565

    class SocketProperties:
        MAX_BUFF_SIZE = 40960

    class LoggerProperties:
        WRITE_LOG_FILE = False
