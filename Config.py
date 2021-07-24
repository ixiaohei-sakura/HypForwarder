class Config:
    class LocalProperties:
        host = "0.0.0.0"
        port = 25565

    class TargetProperties:
        # host = "mc.hypixel.net"  # 等效于下面的
        # host = "172.65.230.98"  # 等效与上面的
        host = "127.0.0.1"
        port = 25565

    class SocketProperties:
        maxBuffSize = 40960

    class LoggerProperties:
        writeLogFiles = False
