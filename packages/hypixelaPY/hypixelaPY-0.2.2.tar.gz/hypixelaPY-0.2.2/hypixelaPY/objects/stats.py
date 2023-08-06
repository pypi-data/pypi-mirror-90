from .. import utils


class KillsDeaths:
    def __init__(self, kills, deaths):
        self.kills = kills
        self.deaths = deaths
        self.ratio = utils.get_ratio(kills, deaths)

    def increase(self, *, amount: int = 0):
        return utils.get_increase(self.kills, self.deaths, amount=amount)


class WinsLosses:
    def __init__(self, wins, losses):
        self.wins = wins
        self.losses = losses
        self.ratio = utils.get_ratio(wins, losses)

    def increase(self, *, amount: int = 0):
        return utils.get_increase(self.wins, self.losses, amount=amount)


class FinalKillsDeaths:
    def __init__(self, kills, deaths):
        self.kills = kills
        self.deaths = deaths
        self.ratio = utils.get_ratio(kills, deaths)

    def increase(self, *, amount: int = 0):
        return utils.get_increase(self.kills, self.deaths, amount=amount)
