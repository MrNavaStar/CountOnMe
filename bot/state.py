import dbm


class State:

    def __init__(self):
        self.score = 0
        self.lastAuthor = None
        self.highestScore = 0
        self.channelId = 0
        self.role = "null"
        self.updated = False

    def save(self):
        with dbm.open("bot_state", "c") as data:
            data["score"] = self.score.__str__()
            data["highestScore"] = self.highestScore.__str__()
            data["channelId"] = self.channelId.__str__()
            data["role"] = self.role.__str__()

    def incrementScore(self):
        self.score += 1
        if self.score > self.highestScore:
            self.highestScore += 1
        self.save()

    def resetScore(self):
        self.score = 0
        self.lastAuthor = None
        self.save()

    def setLastAuthor(self, author):
        self.lastAuthor = author
        self.save()

    def setChannel(self, channelId):
        self.channelId = channelId
        self.save()
