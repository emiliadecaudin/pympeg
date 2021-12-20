# --- Standard Library Imports ------------------------------------------------------- #

from glob import glob
import os
from pydoc import pager
import re
import subprocess

# --- Pip Library Imports ------------------------------------------------------------ #

import inquirer

# --- Internal Imports --------------------------------------------------------------- #

import util

# --- Sub Routines ------------------------------------------------------------------- #


def get_paths(base_path: str, recursive: bool, pattern: str) -> list[str]:

    relative_paths = glob(pattern, root_dir=base_path, recursive=recursive)

    absolute_paths = []

    for path in relative_paths:

        path = os.path.join(base_path, path)
        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        if os.path.isfile(path):

            absolute_paths.append(path)

    return absolute_paths


def probe(path: str) -> str:

    ffprobe_process = subprocess.run(
        ["ffprobe", "-hide_banner", path], capture_output=True, text=True
    )
    return ffprobe_process.stderr


def filter_probe(raw_probe: str) -> list[str] | None:

    filtered_probe = re.findall(
        "(^.*Input.*$|^.*Duration.*$|^.*Stream.*$)", raw_probe, re.MULTILINE
    )

    match len(filtered_probe):
        case 0:
            return None
        case 1:
            return filtered_probe[0].strip()
        case 2:
            return [filtered_probe[0].strip(), "└───" + filtered_probe[1].strip()]
        case 3:
            return [
                filtered_probe[0].strip(),
                "└───" + filtered_probe[1].strip(),
                "   └───" + filtered_probe[2].strip(),
            ]

    decorated_probe = [filtered_probe[0].strip(), "└──┬" + filtered_probe[1].strip()]
    decorated_probe += ["   └──┬" + filtered_probe[2].strip()] + [
        "      ├" + line.strip() for line in filtered_probe[3:]
    ]

    return decorated_probe


# --- Routines ----------------------------------------------------------------------- #


def ffprobe():

    questions = [
        inquirer.Path(
            name="path",
            message='Enter the relative path where the files you would like to probe are located Default is "."',
            default=".",
            path_type=inquirer.Path.DIRECTORY,
            exists=True,
        ),
        inquirer.List(
            name="recursive",
            message="Check subfolders for files",
            choices=["Yes", "No"],
            carousel=True,
        ),
        inquirer.Text(
            name="pattern",
            message='Enter a pattern to match files against. Default is "**"',
            default="**",
            validate=util.validate_pattern,
        ),
    ]

    if responses := inquirer.prompt(questions):

        responses["recursive"] = True if responses["recursive"] == "Yes" else False

        paths = get_paths(
            base_path=responses["path"],
            recursive=responses["recursive"],
            pattern=responses["pattern"],
        )

        if len(paths) == 0:

            print(
                f"\n{util.ERROR_PREFIX} No files matching pattern \"{responses['pattern']}\" were found in directory \"{responses['path']}\"."
            )

        else:

            filtered_probes = []

            for path in paths:

                if filtered_probe := filter_probe(probe(path)):

                    filtered_probes.append(filtered_probe)

            if len(filtered_probes) == 0:

                print(
                    f"\n{util.ERROR_PREFIX} No probable files matching pattern \"{responses['pattern']}\" were found in directory \"{responses['path']}\"."
                )

            else:

                combined_probes = ""

                for filtered_probe in filtered_probes:

                    combined_probes += "\n".join(filtered_probe)
                    combined_probes += "\n\n"

                pager(combined_probes.strip())
