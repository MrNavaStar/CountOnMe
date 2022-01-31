import json


class State:

    def __init__(self):
        self.score = 0
        self.lastAuthor = None
        self.highestScore = 0
        self.channelId = None
        self.role = None
        self.updated = False

    def save(self):
        data = {
            "score": self.score,
            "highestScore": self.highestScore,
            "channelId": self.channelId,
            "role": self.role
        }

        with open("bot/state.json", "w") as json_file:
            json_file.write(json.dumps(data))

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
