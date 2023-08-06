from __init__ import __version__
from colorama import init
import re
init()

# color = "\033[36m"
# color2 = "\033[41m"
# color3 = "\033[33m"
# went = "\033[0m"

__version__ = __version__.replace("a", " \033[41m Alpha ") \
                         .replace("b", " \033[43m\033[30m Beta ")

# __version__ = f"{color}v{color3}{__version__}"
print(f"v{__version__} ")
