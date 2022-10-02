#!/usr/bin/env python

import os
from setuptools import setup, find_namespace_packages
import platform

with open("APPNAME", "r") as _f:
    appname = _f.read()

system = platform.system()
if system == "Linux":
    from xdg import BaseDirectory
    desktop_file_directory = os.path.join(
        BaseDirectory.xdg_data_home,
        "applications",
    )
    icon_file_directory = os.path.join(
        BaseDirectory.xdg_data_home,
        "icons",
        appname,
    )
    data_files = [
        (desktop_file_directory, [desktop_file_name]),
        (icon_file_directory, ["src/{}/images/icon.png".format(appname)])
    ],
elif system == "Darwin":
    data_files = []
    pass
elif system == "Windows":
    data_files = []
    pass
else:
    print("Unsupported system {}".format(system))

description = (
    "Sends notifications at configurable intervals to look away from screen"
)
desktop_file_name = "{}.desktop".format(appname)
with open("README.md", "r", encoding="utf-8") as _f:
    long_description = _f.read()
with open("VERSION", "r") as _f:
    version = _f.read()
with open("VENV_DIR", "r") as _f:
    venv = _f.read()

setup(
    name=appname,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LyuboslavAngelov/eyecare-reminder",
    author="Lyuboslav Angelov",
    author_email="lyuboslav.angelov@gmail.com",
    license="GNU GPLv3",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "{}.sounds".format(appname): ["*.wav"],
        "{}.images".format(appname): ["*.png"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": [
            "{appname}={appname}.main:main".format(appname=appname)
        ],
    },
    data_files=data_files,
    keywords="eye eyecare reminder notification timer",
    python_requires=">=3.8",
)
