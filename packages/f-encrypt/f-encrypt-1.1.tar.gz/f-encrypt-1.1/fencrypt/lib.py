""" Common Code """
import os
import sys
from getpass import getpass
from pathlib import Path


def get_config():
    """ Return dictionary of config specified by environment variables """
    return {
        "KEY": _environ("F_ENCRYPT_KEY", None),
        "SILENT": (_environ("F_ENCRYPT_SILENT") == "true"),
        "VERBOSITY": int(_environ("F_ENCRYPT_VERBOSITY", "1")),
        "OUTPUT_SUFFIX": _environ("F_ENCRYPT_OUTPUT_SUFFIX", ".ct"),
        "RM": _environ("F_ENCRYPT_RM", "false")
    }


def error(msg, exit=True):
    """ Print an error """
    sys.stderr.write(f"ERROR - {msg}\n")
    if exit:
        sys.exit(1)


def echo(msg, verbose=1):
    """ Print to stdout """
    if verbose <= get_config()["VERBOSITY"]:
        sys.stdout.write(f"{msg}\n")


def _environ(name, default="false"):
    """ Return the lower case value of an environment var if set, else its default """
    return os.environ[name].lower() if name in os.environ else default


def validate_path(path, encrypt=True):
    """ Ensure that a given path to a file exists and check if it ends in SUFFIX (then prompt)

        When encrypt=True, checks the output suffix to verify
    """
    path_obj = Path(path)
    if not path_obj.exists():
        error(f"File not found: {path}", exit=True)
    if not path_obj.is_file():
        error(f"{path} must be a file", exit=True)
    config = get_config()
    suffix = config["OUTPUT_SUFFIX"]
    if path.endswith(suffix) and not config["SILENT"] and encrypt:
        echo(f'{path} ends with "{suffix}" and may already be encrypted - Continue? [y/N]')
        resp = input().lower()
        if resp != "y":
            error(f"Exiting because {path} ends with {suffix}", exit=True)
    echo(f"Input path = {path}", 5)


def get_key(key):
    """ If key is none, prompt for a password. If silent is on, throw an error """
    if key:
        return key
    config = get_config()
    if config["SILENT"]:
        error("No key with F_ENCRYPT_SILENT=true. Use --key or F_ENCRYPT_KEY", exit=True)
    return getpass(prompt="Enter Key: ")


def get_output(path, output):
    """ Return the output path to use, and validate if user really wants to overwrite a file """
    config = get_config()
    if output is None:
        suffix = config["OUTPUT_SUFFIX"]
        if path.endswith(suffix):
            # Remove the suffix
            output = path[:-len(suffix)]
        else:
            # Add the suffix
            output = f"{path}{suffix}"
    if not Path(output).exists():
        # no prompt needed, the file didn't already exist
        echo(f"Output path = {output}", 5)
        return output
    if config["SILENT"]:
        # do not prompt if silent mode is enabled
        return output
    echo(f"WARNING - {output} exists - Overwrite? [y/N]")
    resp = input().lower()
    if resp != "y":
        error(f"Exiting because {output} exists", exit=True)
    echo(f"Output path = {output}", 5)
    return output


def delete_file(path, keep):
    """ Delete the file at the given path """
    config = get_config()
    if not keep or condfig['RM'].lower() == "true":
        echo(f"Deleting {path}", 2)
        os.remove(path)
