import logging
from colorama import init, Fore, Style

init(autoreset=True)  # инициализируем colorama

class ColorFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.levelno >= logging.ERROR:
            return Fore.RED + msg + Style.RESET_ALL
        elif record.levelno == logging.INFO:
            return Fore.GREEN + msg + Style.RESET_ALL
        return msg  # для других уровней без цвета

logger = logging.getLogger('tictactoe_bot')
logger.setLevel(logging.DEBUG)

formatter = ColorFormatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)