import json
import requests
from steamplus.startup import oldData


def init():
    """Generates cache data (Run this on startup)"""
    data = []
    newData = []
    page = 0
    while data != {}:
        data = requests.get(f"https://steamspy.com/api.php?request=all&page={page}").json()
        for i in data.values():
            newData.append(i)
        page += 1
    with open("steamplus.json", "w+") as f:
        json.dump(newData, f, ensure_ascii=True, indent=4)
    newData = loadJson()
    heapSort(newData)
    newDataKeys = [i[0] for i in newData]
    heapSort(oldData)
    oldDataKeys = [i[0] for i in oldData]
    returnData = []
    for i in newDataKeys:
        try:
            if i in oldDataKeys:
                dataNew = newData[binarySearch(newDataKeys, i, setup=True)][1]
                dataOld = oldData[binarySearch(oldDataKeys, i, setup=True)][1]
                dataReturn = {
                    "appid": dataNew["appid"],
                    "name": dataNew["name"],
                    "release_date": dataOld["release_date"],
                    "english": dataOld["english"],
                    "developer": dataNew["developer"],
                    "publisher": dataNew["publisher"],
                    "platforms": dataOld["platforms"],
                    "required_age": dataOld["required_age"],
                    "categories": dataOld["categories"],
                    "genres": dataOld["genres"],
                    "steamspy_tags": dataOld["steamspy_tags"],
                    "achievements": dataOld["achievements"],
                    "positive_ratings": dataNew["positive"],
                    "negative_ratings": dataNew["negative"],
                    "average_playtime": dataNew["average_forever"],
                    "median_playtime": dataNew["median_forever"],
                    "price": int(dataNew["price"]) / 100,
                    "initialprice": int(dataNew["initialprice"]) / 100,
                    "discount": dataNew["discount"],
                    "ccu": dataNew["ccu"],
                    "owners": sum([int(i) for i in dataNew["owners"].replace(",", "").split(" .. ")]) // 2
                }
                returnData.append(dataReturn)
            else:
                dataNew = newData[binarySearch(newDataKeys, i, setup=True)][1]
                dataReturn = {
                    "appid": dataNew["appid"],
                    "name": dataNew["name"],
                    "release_date": "unknown",
                    "english": "unknown",
                    "developer": dataNew["developer"],
                    "publisher": dataNew["publisher"],
                    "platforms": "unknown",
                    "required_age": "unknown",
                    "categories": "unknown",
                    "genres": "unknown",
                    "steamspy_tags": "unknown",
                    "achievements": "unknown",
                    "positive_ratings": dataNew["positive"],
                    "negative_ratings": dataNew["negative"],
                    "average_playtime": dataNew["average_forever"],
                    "median_playtime": dataNew["median_forever"],
                    "price": int(dataNew["price"]) / 100,
                    "initialprice": int(dataNew["initialprice"]) / 100,
                    "discount": dataNew["discount"],
                    "ccu": dataNew["ccu"],
                    "owners": sum([int(i) for i in dataNew["owners"].replace(",", "").split(" .. ")]) // 2
                }
                returnData.append(dataReturn)
        except:
            pass
    with open("steamplus.json", "w+") as f:
        json.dump(returnData, f, ensure_ascii=True, indent=4)


def loadJson(sortID=True, file="steamplus.json"):
    """Reads data file, returns a dict of appid's with each appid containing game info"""
    if sortID is True:
        sortType = "appid"
    else:
        sortType = "name"
    with open(file) as f:
        data = json.load(f)
        returnData = [(i[sortType], i) for i in data]
        for i in range(len(returnData)):
            if i is dict:
                returnData.pop(i)
        return returnData


def heap(data, size, index):
    """heapify subtree's in binary tree"""
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2
    if type(data[0]) != tuple:
        if left < size and data[largest] < data[left]:
            largest = left
        if right < size and data[largest] < data[right]:
            largest = right
    else:
        if left < size and data[largest][0] < data[left][0]:
            largest = left
        if right < size and data[largest][0] < data[right][0]:
            largest = right
    if largest != index:
        data[index], data[largest] = data[largest], data[index]
        heap(data, size, largest)


def heapSort(data):
    """Sorts data using heapify (heapsort algorithm)"""
    size = len(data)
    for i in range(size // 2 - 1, -1, -1):
        heap(data, size, i)
    for i in range(size - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        heap(data, i, 0)


def binarySearch(data, target, low=0, high=0, setup=False):
    """Searches data with a recursive binary search algorithm (list must be sorted)"""
    if setup is True:
        high = len(data) - 1
        low = 0
    if high >= low:
        mid = (high + low) // 2
        if type(data[0]) is tuple:
            if data[mid][0] == target:
                return mid
            elif data[mid][0] > target:
                return binarySearch(data, target, low, mid - 1)
            else:
                return binarySearch(data, target, mid + 1, high)
        else:
            if data[mid] == target:
                return mid
            elif data[mid] > target:
                return binarySearch(data, target, low, mid - 1)
            else:
                return binarySearch(data, target, mid + 1, high)
    else:
        return "Item not found"
