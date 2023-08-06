import paramiko

class _FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(_FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)