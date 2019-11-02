import multiprocessing
from time import sleep
import json
from rtgraph.core.constants import Constants
from rtgraph.common.logger import Logger as Log

TAG = "Parser"


class ParserProcess(multiprocessing.Process):
    """
    Process to parse incoming data, parse it, and then distribute it to graph and storage.
    """
    def __init__(self,
                 data_queue,
                 store_reference=None,
                 split=Constants.csv_delimiter,
                 consumer_timeout=Constants.parser_timeout_ms):
        """

        :param data_queue: Reference to Queue where processed data will be put.
        :type data_queue: multiprocessing Queue.
        :param store_reference: Reference to CSVProcess instance, if needed.
        :type store_reference: CSVProcess (multiprocessing.Process)
        :param split: Delimiter in incoming data.
        :type split: str.
        :param consumer_timeout: Time to wait after emptying the internal buffer before next parsing.
        :type consumer_timeout: float.
        """
        multiprocessing.Process.__init__(self)
        self._exit = multiprocessing.Event()
        self._in_queue = multiprocessing.Queue()
        self._out_queue = data_queue
        self._consumer_timeout = consumer_timeout
        self._split = split
        self._store_reference = store_reference
        self._leftover = ''
        Log.d(TAG, "Process ready")

    def add(self, txt):
        """
        Adds new raw data to internal buffer.
        :param txt: Raw data comming from acquisition process.
        :type txt: basestring.
        :return:
        """
        self._in_queue.put(txt)

    def run(self):
        """
        Process will monitor the internal buffer to parse raw data and distribute to graph and storage, if needed.
        The process will loop again after timeout if more data is available.
        :return:
        """
        Log.d(TAG, "Process starting...")
        while not self._exit.is_set():
            self._consume_queue()
            sleep(self._consumer_timeout)
        # last check on the queue to completely remove data.
        self._consume_queue()
        Log.d(TAG, "Process finished")

    def stop(self):
        """
        Signals the process to stop parsing data.
        :return:
        """
        Log.d(TAG, "Process finishing...")
        self._exit.set()

    def _consume_queue(self):
        """
        Consumer method for the queues/process.
        Used in run method to recall after a stop is requested, to ensure queue is emptied.
        :return:
        """
        while not self._in_queue.empty():
            queue = self._in_queue.get(timeout=self._consumer_timeout)
            self._parse_queue(queue)

    def _parse_queue(self, queue):
        """
        Parses incoming data and distributes to external processes.
        :param time: Timestamp.
        :type time: float.
        :param line: Raw data coming from acquisition process.
        :type line: basestring.
        :return:
        """
        # list of possible stringified lists, might be split across stream
        data = queue.split("\n")
        if len(self._leftover) > 0:
            data[0] = self._leftover + data[0]
            print("recombined")
        for datum in data:
            try:
                datapoint = json.loads(datum)
                self._out_queue.put((datapoint[0], datapoint[1]))
                if self._store_reference is not None:
                    self._store_reference.add(datapoint[0], datapoint[1])
            except json.decoder.JSONDecodeError:
                self._leftover = datum
