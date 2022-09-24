import os
import psutil
import subprocess
import yaml
from yaml.loader import SafeLoader


def checkIfProcessRunning(process_name):
    """Check if there is any running process that contain
    the given name process_name.

    Args:
        process_name (str): The process name to check for.

    Returns:
        bool: Whether the process is running or not.
    """
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            pass

    return False


def checkIfWindowRunning(window_name, output=None):
    """Check if there are any windows open that contain the given window_name

    Args:
        window_name (str): The window name to check for.
        output (str, optional): Optionally, provide an output of a command
            that lists the currently open windows.

    Returns:
        bool: Whether there are any windows open that contain the given name.
    """
    if not output:
        output = subprocess.check_output(["xwininfo", "-tree", "-root"])
    if window_name in str(output):
        return True
    else:
        return False


def import_yaml(path):
    """Imports a yaml file.

    Returns:
        dict: The contents of the yaml file as a dict object.
    """
    with open(path) as _f:
        data = {}
        try:
            data = yaml.load(_f, Loader=SafeLoader)
        except yaml.YAMLError:
            # we pass as user will be notified of invalid config
            # when empty dict is returned
            pass
        return data


def write_yaml(path, data):
    """Write the given data as a yaml file at the given path.

    Args:
        path (str): The path to write the yaml file at.
        data (dict): The data to write into the yaml file.
    """
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    with open(path, "w") as _f:
        yaml.dump(data, _f)


def convert_ms_to_seconds(value):
    """Convert a time value from milliseconds into seconds.

    Args:
        value (float): The time value to convert.

    Returns:
        float: The interval value converted into seconds.
    """
    return value / 1000


def convert_seconds_to_ms(value):
    """Convert a time value from seconds into milliseconds.

    Args:
        value (float): The time value to convert.

    Returns:
        float: The time value converted into milliseconds.
    """
    return value * 1000


def play_sound(sound_file):
    """Play a sound.

    Args:
        sound_file (str): The file path of the sound to play.
            Must have .wav file extension
    """
    ext = sound_file.split(".")[-1]
    if not ext == "wav":
        raise RuntimeError("Unsupported audio extension .{}".format(ext))
    subprocess.Popen(("aplay", sound_file))
