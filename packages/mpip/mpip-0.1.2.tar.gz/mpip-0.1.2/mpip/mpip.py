import tempfile
import os
import subprocess
import sys
from contextlib import contextmanager
from io import TextIOWrapper
from os import PathLike
from pathlib import Path
from typing import Union, TextIO

import fire
import rich
from pipeline import execution_pipeline
from pkg_resources import parse_requirements

REQUIREMENTS_FILE = os.path.join(os.getcwd(), "requirements.txt")
DEFAULTS = {
    "requirements": REQUIREMENTS_FILE,
    "quiet": False,
    "output": "stderr",
}


def process_short_flags(params: dict) -> dict:
    short_flags_map = {
        "r": "requirements",
        "q": "quiet",
        "o": "output",
        "y": "yes",
    }
    for short_flag, long_flag in short_flags_map.items():
        short_flag_param = params.get(short_flag, None)
        if short_flag_param:
            if params.get(long_flag, None):
                rich.print(
                    f"[bold red]`mpip` only accepts one of the flags -{short_flag} and --{long_flag}.[/bold red]",
                    file=sys.stderr,
                )
                exit(1)
            else:
                params[long_flag] = short_flag_param
    return params


def get_defaults(params: dict) -> dict:
    for key in DEFAULTS.keys():
        if not params[key]:
            params[key] = DEFAULTS[key]
    return params


def validate_command(params: dict) -> dict:
    valid_commands = {"install", "uninstall"}
    if not params["command"] in {"install", "uninstall"}:
        rich.print(
            f"[bold red]Expected command to be one of[/bold red] {valid_commands}[bold red]; got `{params['command']}` instead.[/bold red]",
            file=sys.stderr,
        )
        exit(1)
    return params


def validate_requirements(params: dict) -> dict:
    requirements = params["requirements"]
    requirements = Path(requirements)
    if requirements.is_dir():
        rich.print(f"[bold red]`{requirements}` is a directory.[/bold red]", file=sys.stderr)
    elif not requirements.parent.exists():
        rich.print(
            f"[bold red]Cannot create requirements file; `{requirements.parent}` does not exist.[/bold red]",
            file=sys.stderr,
        )
        exit(1)
    params["requirements"] = Path(requirements)
    return params


def validate_output(params: dict) -> dict:
    output_getter_mapping = {
        "stderr": lambda x: sys.stderr,
        "stdout": lambda x: sys.stdout,
    }
    output = str(params["output"])
    params["output"] = output_getter_mapping.get(output, lambda x: Path(output))(output)
    return params


@contextmanager
def maybe_open_file(maybe_path: Union[PathLike, TextIOWrapper, TextIO]):
    did_open = False
    if isinstance(maybe_path, (TextIOWrapper, tempfile.TemporaryFile().__class__)):
        yield maybe_path
    else:
        try:
            f = open(maybe_path, "w")
            did_open = True
            yield f
        finally:
            if did_open:
                f.close()


def rprint(content, file):
    if isinstance(file, tempfile.TemporaryFile().__class__):
        # for when "quiet" flag is enabled
        return
    with maybe_open_file(file) as f:
        rich.print(content, file=f)


def name_from_req(requirement):
    name = f'{requirement.name}[{",".join(requirement.extras)}]' if requirement.extras else requirement.name
    return name.lower()


def run(*args, stdout=sys.stdout, stderr=sys.stderr):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    with maybe_open_file(stdout) as stdout:
        with maybe_open_file(stderr) as stderr:
            # Some file descriptors want bytes and others want strings.
            # Most runs will use stdout, stderr which wants strings.
            try:
                [stdout.write(out.decode()), stderr.write(err.decode()), stdout.flush(), stderr.flush()]
            except TypeError:
                # needed with --quiet flag
                [stdout.write(out), stderr.write(err), stdout.flush(), stderr.flush()]
            return proc.returncode


@execution_pipeline(pre=[process_short_flags, get_defaults, validate_requirements, validate_output, validate_command])
def mpip(command, *args, quiet=False, requirements=None, output=None, yes=False, **kwargs):
    """
    mpip

    A thin wrapper around `pip` which adjusts your `requirements.txt` as you install or uninstall dependencies. All
    long flags have a corresponding short flag, e.g. `--out stdout` and `-o stdout` provide the same functionality.

    Example:
        - `mpip install django djangorestframework`
        - `mpip uninstall django djangorestframework`
    Args:
        command: install or uninstall
        args: list of packages to install or uninstall.

    :param quiet: Whether to output information to the file specified by the `output` parameter. Defaults to False
    :param requirements: Path to your requirements.txt file. Defaults to `./requirements.txt`.
    :param output: File path to output text from the script. Defaults to stderr, and stdout is a valid option.
    :param yes: Confirm without prompting for user input.
    """
    if quiet:
        output, yes = tempfile.TemporaryFile(), True
    if not requirements.exists():
        rprint(f"[bold cyan]Creating new `requirements.txt` file at `{requirements}`.[/bold cyan]", file=output)
        with open(requirements, "w"):
            pass

    y = ("-y",) if yes and command == "uninstall" else ()
    res = run("pip", command, *y, *args, stdout=output, stderr=output)
    if not res == 0:
        rprint(f"[red]ERROR: Command failed; not modifying `requirements.txt`.[/red]", file=output)
        exit(1)

    adjusted_requirements = {}
    with open(requirements) as r:
        for req in parse_requirements(r.readlines()):
            adjusted_requirements[req.name.lower()] = req

    for req in parse_requirements(args):
        if command == "install":
            adjusted_requirements[req.name.lower()] = req
        else:
            adjusted_requirements.pop(req.name.lower(), None)

    if adjusted_requirements:
        requirements_contents = "\n".join(
            sorted([str(f"{name_from_req(req)}{req.specifier}") for req in adjusted_requirements.values()])
        )
        with open(requirements, "w") as f:
            f.write(f"{requirements_contents}\n")
    elif requirements.exists():
        os.remove(requirements)


def main():
    fire.Fire(mpip)


if __name__ == "__main__":
    main()
