# --- Pip Library Imports ------------------------------------------------------------ #

from blessed import Terminal

# --- Constants ---------------------------------------------------------------------- #

TERMINAL = Terminal()
ERROR_PREFIX = f"{TERMINAL.red}>>{TERMINAL.normal}{TERMINAL.bold}"

# --- Functions ---------------------------------------------------------------------- #


def validate_pattern(prev_answers: dict, current: str) -> bool:

    return True

    # return current == "*" or re.match("^\.[a-zA-Z0-9]+$", current)


def get_file_paths(path: str, extension: str) -> list:

    return []
