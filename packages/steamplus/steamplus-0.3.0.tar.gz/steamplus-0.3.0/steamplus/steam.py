from collections import Counter
import requests
from steamplus.tools import loadJson
from steamplus.statistics import mode, median, mean
from pprint import pprint


class Statistics:
    """Statistics of a sample of the database"""
    def __init__(self, name=None, _type=None):
        # data
        if name is None and _type is None:
            self.data = loadJson()
        else:
            self.data = loadJson()
            self.data = [i for i in self.data if name in i[1][_type]]

        # genres
        self.genres = [j for x in (i[1]["genres"].split(";") for i in self.data) for j in x]
        self.genreCounts = dict(Counter(self.genres))
        self.modeGenre = mode(self.genres)

        # categories
        self.categories = [j for x in (i[1]["categories"].split(";") for i in self.data) for j in x]
        self.categoryCounts = dict(Counter(self.categories))
        self.modeCategory = mode(self.genres)

        # steamspy tags
        self.ssTags = [j for x in (i[1]["steamspy_tags"].split(";") for i in self.data) for j in x]
        self.ssTagCounts = dict(Counter(self.ssTags))
        self.modeSsTag = mode(self.ssTags)

        # platforms
        self.platforms = [j for x in (i[1]["platforms"].split(";") for i in self.data) for j in x]
        self.platformCounts = dict(Counter(self.platforms))
        self.modePlatform = mode(self.platforms)

        # english
        self.english = [i[1]["english"] for i in self.data if i[1]["english"] != "unkown"]
        self.englishCounts = dict(Counter(self.english))
        self.englishCounts["english"] = self.englishCounts.pop(1)
        self.englishCounts["non-english"] = self.englishCounts.pop(0)

        # price
        self.f2p = len([i[1]["price"] for i in self.data if i[1]["price"] == 0])
        self.prices = [i[1]["price"] for i in self.data if i[1]["price"] != 0]
        self.meanPrice = round(mean(self.prices), 2)
        self.medianPrice = round(median(self.prices), 2)
        self.modePrice = mode(self.prices)
        self.initialPrices = [i[1]["initialprice"] for i in self.data if i[1]["initialprice"] != 0]
        self.meanInitialPrice = round(mean(self.initialPrices), 2)
        self.medianInitialPrice = round(median(self.initialPrices), 2)
        self.modeInitialPrice = mode(self.prices)

        # discount
        self.discounts = [int(i[1]["discount"]) for i in self.data if int(i[1]["discount"]) != 0]
        self.meanDiscount = round(mean(self.discounts), 2)
        self.medianDiscount = round(median(self.discounts), 2)
        self.modeDiscount = mode(self.discounts)

        # achievements
        self.achievements = [i[1]["achievements"] for i in self.data if i[1]["achievements"] != "unknown"]
        self.meanAchievements = int(mean(self.achievements))
        self.medianAchievements = int(round(median(self.achievements), 0))
        self.modeAchievements = mode(self.achievements)

        # owners
        self.owners = [i[1]["owners"] for i in self.data]
        self.meanOwners = int(mean(self.owners))

        # ccu
        self.ccu = [i[1]["ccu"] for i in self.data]
        self.meanCCU = int(mean(self.ccu))

        # developer
        self.developers = [i[1]["developer"] for i in self.data]
        self.developerCounts = dict(Counter(self.developers))
        # self.modeDeveloper = mode(self.developers) //takes to long to run

        # publisher
        self.publishers = [i[1]["publisher"] for i in self.data]
        self.publisherCounts = dict(Counter(self.developers))
        # self.modePublisher = mode(self.publishers) //takes to long to run

        # rating
        self.positiveRating = [i[1]["positive_ratings"] for i in self.data]
        self.negativeRating = [i[1]["negative_ratings"] for i in self.data]
        self.ratingRatio = [round(self.positiveRating[i] / ((self.positiveRating[i] + self.negativeRating[i]) / 100), 2)
                            for i in range(0, len(self.positiveRating)) if self.positiveRating[i] != 0 and
                            self.negativeRating != 0]
        self.meanRatingRatio = round(mean(self.ratingRatio), 2)
        self.medianRatingRatio = round(median(self.ratingRatio), 2)


class Game:
    """Statistics of a particular game"""
    def __init__(self, appid):
        self.appid = appid
        self.data = requests.get(f"http://steamspy.com/api.php?request=appdetails&appid={self.appid}").json()
        self.name = self.data["name"]
        self.developer = self.data["developer"]
        self.publisher = self.data["publisher"]
        self.positiveRatings = self.data["positive"]
        self.negativeRatings = self.data["negative"]
        self.ratingRatio = self.negativeRatings + self.negativeRatings / 100 * self.positiveRatings
        self.owners = sum([int(i) for i in self.data["owners"].replace(",", "").split(" .. ")]) // 2
        self.average = self.data["average_forever"]
        self.median = self.data["median_forever"]
        self.discountPrice = round(int(self.data["price"]) / 100, 2)
        self.price = round(int(self.data["initialprice"]) / 100, 2)
        self.discount = f"{self.data['discount']}%"
        self.ccu = self.data["ccu"]
        self.languages = self.data["languages"].split(", ")
        self.genre = self.data["genre"]
        self.tags = self.data["tags"].keys()
        self.steamstoreData = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}").json()[f"{appid}"]["data"]
        self.about = self.steamstoreData["about_the_game"]
        self.description = self.filter(self.steamstoreData["detailed_description"])
        self.headerImgURL = self.steamstoreData["header_image"]
        self.backgroundURL = self.steamstoreData["background"]
        self.platforms = list(self.steamstoreData["platforms"].keys())
        self.screenshotURLS = [i["path_thumbnail"] for i in self.steamstoreData["screenshots"]]

    @staticmethod
    def filter(text):
        text = text.replace("<br>", "")
        text = text.replace("<br/>", "")
        text = text.replace("</br>", "")
        text = text.replace('<ul class="bb_ul">', "")
        text = text.replace("</ul>", "")
        text = text.replace("<li>", "")
        text = text.replace("</li>", "")
        text = text.replace("<strong>", "")
        text = text.replace("</strong>", "")
        text = text.replace("<i>", "")
        text = text.replace("</i>", "")
        text = text.replace("<h1>", "")
        text = text.replace("</h1>", "")
        text = text.replace("<h2>", "")
        text = text.replace("</h2>", "")
        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        text = text.replace("&quot;", "")
        text = " ".join(text.split())
        return text
