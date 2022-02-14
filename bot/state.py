import dbm


class State:

    def __init__(self):
        self.score = 0
        self.lastAuthor = None
        self.highestScore = 0
        self.lowestScore = 0
        self.channelId = 0
        self.roleId = 0
        self.updated = False
        self.direction = 1
        self.amountSinceLastSwitch = 0

    def save(self):
        with dbm.open("bot_state", "c") as data:
            data["score"] = self.score.__str__()
            data["highestScore"] = self.highestScore.__str__()
            data["lowestScore"] = self.lowestScore.__str__()
            data["channelId"] = self.channelId.__str__()
            data["role"] = self.roleId.__str__()

    def setDirection(self, direction):
        self.direction = direction
        self.amountSinceLastSwitch = 10

    def incrementScore(self):
        self.score += self.direction
        self.amountSinceLastSwitch -= 1
        if self.score > self.highestScore:
            self.highestScore += 1
        if self.score < self.lowestScore:
            self.lowestScore -= 1
        self.save()

    def resetScore(self):
        self.score = 0
        self.amountSinceLastSwitch = 0
        self.direction = 1
        self.lastAuthor = None
        self.save()

    def setLastAuthor(self, author):
        self.lastAuthor = author
        self.save()

    def setChannel(self, channelId):
        self.channelId = channelId
        self.save()

    def setRole(self, id):
        self.roleId = id
        self.save()
