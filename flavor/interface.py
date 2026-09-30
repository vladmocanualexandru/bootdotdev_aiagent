
from termcolor import colored
from flavor.colors import COLORS

LOGO = "\n".join([
    "",
    "                                                                                      |\\__/,|   (`\\",
    colored("█▀█  ▀█▀ █   █   █ █      █▀▀ █▀█ █▀▄ █▀▀", COLORS.LOGO_LINE_1)+"                                             |_ _  |.--.) )",
    colored("█▀▀█  █  █   █   ▀█▀      █   █ █ █ █ █▀ ", COLORS.LOGO_LINE_2)+"                                             ( T   )     /",
    colored("▀▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀  ▀       ▀▀▀ ▀▀▀ ▀▀  ▀▀▀", COLORS.LOGO_LINE_3)+"                                             (((^_(((/(((_/",
    colored("───────────────────────────────────────────────────────────────────────────────────────────────────────", (64,64,64)),
    "",
])

HELP = "\n".join([
    "",
    colored("[value] - type prompt", COLORS.HELP),
    colored("/h - help; show this guide", COLORS.HELP),
    colored("/r - reset; reset conversation", COLORS.HELP),
    colored("/w [value] - set working directory", COLORS.HELP),
    colored("/l - toggle local model", COLORS.HELP),
    colored("/v - toggle verbose", COLORS.HELP),
    colored("/q - quit", COLORS.HELP),
    "",
])
