import numpy as np
import collections
"""
http://code.activestate.com/recipes/68429-ring-buffer/
http://stackoverflow.com/questions/4151320/efficient-circular-buffer

Used deque and saw speedup, O(1) since we don't need 
to access individual elements of the array

"""


class RingBuffer():
    def __init__(self, size_max):

        self._data = collections.deque([0], maxlen=size_max)

    def append(self, value):
        """
        append an element
        :param value:
        """
        self._data.appendleft(value)

    def get_all(self):
        """
        return a list of elements from the oldest to the newest
        """
        return list(self._data)
