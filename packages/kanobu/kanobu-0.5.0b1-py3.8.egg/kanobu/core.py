import locale

if __file__ == "__main__":
    from __init__ import __version__
else:
    from kanobu import __version__


class Kanobu:
    def __init__(self):
        self.lang = locale.getdefaultlocale()[0]
        self.version = f"v{__version__}"
        self.name = "Rock paper scissors"
        self.objects = ["Rock", "Scissors", "Paper"]
        self.kanobu_logo = [
            " _                     _           ",
            "| | ____ _ _ __   ___ | |__  _   _ ",
            "| |/ / _` | '_ \\ / _ \\| '_ \\| | | |",
            "|   < (_| | | | | (_) | |_) | |_| |",
            "|_|\\_\\__,_|_| |_|\\___/|_.__/ \\__,_|",
            "                                   "
        ]

    def game(self, players):
        self.players = players

    def logo(self):
        for item in self.kanobu_logo:
            print(self.blue(item))

    def blue(self, text):
        return f"\033[34m {text}\033[0m"

    def rzaka(self):
        for player in self.players:
            print(f"{player.name} - {self.objects[player.choice - 1]}")
