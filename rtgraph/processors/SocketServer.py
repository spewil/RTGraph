import json
import multiprocessing
from time import time
import socket
from rtgraph.core.constants import Constants
from rtgraph.common.logger import Logger as Log

TAG = "Socket"


class SocketProcess(multiprocessing.Process):
    """
    Socket server
    """
    def __init__(self, parser_process):
        """
        Initialises values for process.
        :param parser_process: Reference to a ParserProcess instance.
        :type parser_process: ParserProcess
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._parser = parser_process
        self._socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                       1)
        self._conn = None
        Log.i(TAG, "Process Ready")

    def open(self, host='', port=45454, timeout=0.01):
        """
        Opens a socket connection to specified host and port
        :param host: Host address to connect to.
        :type host: str.
        :param port: Port number to connect to.
        :type port: int.
        :param timeout: Sets timeout for socket interactions.
        :type timeout: float.
        :return: True if the connection was open.
        :rtype: bool.
        """
        try:
            # self._socket_server.timeout = timeout
            port = int(port)
            self._socket_server.bind((host, port))
            Log.i(TAG, "Socket open {}:{}".format(host, port))
            print("listening on {}:{}".format(
                self._socket_server.getsockname()[0],
                self._socket_server.getsockname()[1]))
            self._socket_server.listen(1)
            self._conn, address = self._socket_server.accept()
            self._conn.setblocking(0)  # non-blocking
            print("accepted from {}".format(address))
            return True
        except socket.timeout:
            Log.w(TAG, "Connection timeout")
        return False

    def run(self):
        """
        Reads the socket until a stop call is made OR client disconnects.
        :return:
        """
        Log.i(TAG, "Process starting...")
        while not self._exit.is_set():
            try:
                # this is set to non-blocking so we can catch errors if no data is present
                packet = self._conn.recv(
                    Constants.SocketServer.buffer_recv_size).decode()
                if len(packet) > 0:
                    # print("len packet: ", len(packet))
                    self._parser.add(packet)
                else:  # client no longer sending data
                    Log.w(TAG, "No incoming data")
                    self.stop()
            except BlockingIOError:  # connection being establish
                pass
        Log.i(TAG, "Process finished")

    def stop(self):
        """
        Signals the process to stop acquiring data.
        :return:
        """
        Log.i(TAG, "Server closing")
        self._conn.close()
        self._socket_server.close()
        self._exit.set()

    @staticmethod
    def get_default_host():
        """
        Returns a list of local host names, localhost, host name and local ip address, if available.
        :return: str list.
        """
        try:
            values = socket.gethostbyaddr(
                socket.gethostbyname(socket.gethostname()))
        except socket.herror:
            values = (None, None, None)

        hostname = values[0]
        hostip = values[2]

        if hostip is not None:
            return [Constants.SocketServer.host_default, hostname, hostip]
        else:
            return [Constants.SocketServer.host_default, hostname]

    @staticmethod
    def get_default_port():
        """
        Returns a list of commonly used socket ports.
        :return: str list.
        """
        return [str(v) for v in Constants.SocketServer.port_default]
