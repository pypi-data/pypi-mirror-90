from .stats import WinsLosses, KillsDeaths


class Blitz:
    def __init__(self, data):
        self.name = "Blitz"
        self.coins = data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("coins", 0)
        self.games_played = data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("games_played", 0)
        self.kills = KillsDeaths(
            data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("kills", 0),
            data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("deaths", 0)
        )
        self.wins = WinsLosses(
            data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("wins", 0),
            data.get("player", {}).get("stats", {}).get("HungerGames", {}).get("deaths", 0)
        )

    def __str__(self):
        return self.name
