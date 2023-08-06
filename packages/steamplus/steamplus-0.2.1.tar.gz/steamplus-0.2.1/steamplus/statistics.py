import copy as cpy
from steamplus.tools import heapSort


def mean(data):
    """Returns mean(average) of data"""
    return sum(data) / len(data) if len(data) != 0 else 0


def mode(data):
    """Returns mode(most common item) of data"""
    return max(set(data), key=data.count) if len(data) != 0 else 0


def median(data):
    """Returns median of data"""
    data = cpy.deepcopy(data)
    heapSort(data)
    return data[(len(data) - 1) // 2] if len(data) % 2 else (data[(len(data) - 1) // 2] + data[
        ((len(data) - 1) // 2) + 1]) / 2

