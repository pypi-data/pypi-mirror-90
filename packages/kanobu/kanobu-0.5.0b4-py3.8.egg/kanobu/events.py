class Win:
    def __init__(self, name):
        self.name = name
        self.fullname = f"\033[31m{name}\033[0m"


class Loss:
    def __init__(self, name):
        self.name = name
        self.fullname = f"\033[32m{name}\033[0m"


class Draw:
    def __init__(self, name):
        self.name = name
        self.fullname = f"\033[33m{name}\033[0m"


class Event:
    def __init__(self, name, localename):
        self.colors = {
            "win": "\033[32m",
            "loss": "\033[31m",
            "draw": "\033[33m"
        }
        self.end = "\033[0m"
        self.tname = localename
        self.name = f"{self.colors[name]}{localename}{self.end}"


if __name__ == "__main__":
    print(Event("win", "победа").name)
