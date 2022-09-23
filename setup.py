#!/usr/bin/env python

import os
from setuptools import setup, find_namespace_packages
from xdg import BaseDirectory


desktop_file_directory = os.path.join(
    BaseDirectory.xdg_data_home,
    "applications",
)
icon_file_directory = os.path.join(
    BaseDirectory.xdg_data_home,
    "icons",
    "eyecare_reminder",
)
description = (
    "Sends notifications at configurable intervals to look away from screen"
)
desktop_file_name = "eyecare_reminder.desktop"
with open("README.md", "r", encoding="utf-8") as _f:
    long_description = _f.read()
with open("VERSION", "r") as _f:
    version = _f.read()
with open("VENV", "r") as _f:
    venv = _f.read()

setup(
    name="eyecare_reminder",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LyuboslavAngelov/eyecare-reminder",  # TODO change
    author="Lyuboslav Angelov",
    author_email="lyuboslav.angelov@gmail.com",
    license="GNU GPLv3",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "eyecare_reminder.sounds": ["*.wav"],
        "eyecare_reminder.images": ["*.png"],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": ["eyecare_reminder=eyecare_reminder.main:main"],
    },
    data_files=[
        (desktop_file_directory, [desktop_file_name]),
        (icon_file_directory, ["src/eyecare_reminder/images/icon.png"])
    ],
    keywords="eye eyecare reminder notification timer",
    python_requires=">=3.8",
)
