from datetime import datetime


class Colours:
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"
    RESET = "\u001b[0m"


def printWithTime(msg):
    print(
        f"{Colours.YELLOW}[ {datetime.now().strftime('%H:%M:%S.%f')[:-3]} ] - {msg}{Colours.RESET}"
    )


def log(msg):
    self.printWithTime(f"{Colours.YELLOW}{msg}")


def success(msg):
    self.printWithTime(f"{Colours.GREEN}{msg}")


def error(msg):
    self.printWithTime(f"{Colours.RED}{msg}")


def warn(msg):  # * Warn of something that needs an action
    printWithTime(f"{Colours.MAGENTA}{msg}")


def alert(msg):  # * Alert of something good/neutral
    printWithTime(f"{Colours.BLUE}{msg}")


def msg(self, msg):
    printWithTime(f"{Colours.CYAN}{msg}")


def logp(i, msg):
    slog(f"[{i}] -> {msg}")


def successp(i, msg):
    success(f"[{i}] -> {msg}")


def errorp(i, msg):
    error(f"[{i}] -> {msg}")


def warnp(i, msg):
    warn(f"[{i}] -> {msg}")


def alertp(i, msg):
    alert(f"[{i}] -> {msg}")


def msgp(i, msg):
    msg(f"[{i}] -> {msg}")
