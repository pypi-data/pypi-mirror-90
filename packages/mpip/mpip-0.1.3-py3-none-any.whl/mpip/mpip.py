import os
import subprocess
import sys
from pathlib import Path

import fire
import rich
from pipeline import execution_pipeline
from pkg_resources import parse_requirements

REQUIREMENTS_FILE = os.path.join(os.getcwd(), "requirements.txt")
DEFAULTS = {
    "requirements": REQUIREMENTS_FILE,
    "quiet": False,
}


def process_short_flags(params: dict) -> dict:
    short_flags_map = {
        "r": "requirements",
        "q": "quiet",
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


def name_from_req(requirement):
    name = f'{requirement.name}[{",".join(requirement.extras)}]' if requirement.extras else requirement.name
    return name.lower()


@execution_pipeline(pre=[process_short_flags, get_defaults, validate_requirements, validate_command])
def mpip(command, *args, quiet=False, requirements=None, yes=False, **kwargs):
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
    :param yes: Confirm without prompting for user input.
    """
    stdout, stderr = sys.stdout, sys.stderr
    if quiet:
        yes, stdout, stderr = True, subprocess.PIPE, subprocess.PIPE
    if not requirements.exists():
        if not quiet:
            rich.print(f"[bold cyan]Creating new `requirements.txt` file at `{requirements}`.[/bold cyan]")
        with open(requirements, "w"):
            pass

    y = ("-y",) if yes and command == "uninstall" else ()
    res = subprocess.run(["pip", command, *y, *args], stdout=stdout, stderr=stderr)
    if not res.returncode == 0:
        rich.print(f"[red]ERROR: Command failed; not modifying `requirements.txt`.[/red]")
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
