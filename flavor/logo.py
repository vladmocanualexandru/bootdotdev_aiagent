
from termcolor import colored
from flavor.colors import COLORS

LOGO = "\n".join([
    "",
    "                                                                       |\\__/,|   (`\\",
    colored("█▀█  ▀█▀ █   █   █ █      █▀▀ █▀█ █▀▄ █▀▀", COLORS.LOGO_LINE_1)+"                              |_ _  |.--.) )",
    colored("█▀▀█  █  █   █   ▀█▀      █   █ █ █ █ █▀ ", COLORS.LOGO_LINE_2)+"                              ( T   )     /",
    colored("▀▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀  ▀       ▀▀▀ ▀▀▀ ▀▀  ▀▀▀", COLORS.LOGO_LINE_3)+"                              (((^_(((/(((_/",
    colored("──────────────────────────────────────────────────────────────────────────────────────", (64,64,64)),
    colored("/working_directory|/w [value] - set working directory", COLORS.HELP),
    colored("/local|/l - toggle local model", COLORS.HELP),
    colored("/verbose|/v - toggle verbose", COLORS.HELP),
    colored("/quit|/q - quit", COLORS.HELP),
    "",
])
