# --- Standard Library Imports ------------------------------------------------------- #

import contextlib

# --- Pip Library Imports ------------------------------------------------------------ #

import inquirer

# --- Internal Imports --------------------------------------------------------------- #

from ffmpeg import ffmpeg
from ffprobe import ffprobe

# --- Main Execution------------------------------------------------------------------ #

if __name__ == "__main__":

    with contextlib.suppress(KeyboardInterrupt):

        question = "Select the type of operation you would like to execute"
        choices = [(ffmpeg.__name__, ffmpeg), (ffprobe.__name__, ffprobe)]

        inquirer.list_input(question, choices=choices)()
