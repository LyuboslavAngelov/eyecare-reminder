SHELL = /bin/bash

VENV_FILE="VENV"
DEPENDENCIES_FILE="BUILD_DEPENDENCIES"
VERSION_FILE="VERSION"

VENV:=$(shell cat $(VENV_FILE))
VERSION:=$(shell cat $(VERSION_FILE))
DEB_PACKAGE_NAME=python3-eyecare-reminder

.PHONY clean-venv:  # Clean the built virtual environment
clean-venv:
	printf "\033[0;36m\n\n--------Cleaning the venv files--------\n\n\n"
	rm -rf ${VENV}
	rm -rf build
	printf "\033[0;36m\n\n--------Finished cleaning the venv files--------\n\n\n"

.PHONY clean-dist:  # Clean the built deb package
	printf "\033[0;36m\n\n--------Cleaning the deb build files--------\n\n\n"
	rm -rf deb_dist
	rm -rf dist
	rm -rf deb
	rm -rf eyecare_reminder.egg-info
	printf "\033[0;36m\n\n--------Finished cleaning the deb build files--------\n\n\n"

.PHONY clean-all:  # Clean all the build directories
clean-all: clean-venv clean-dist

.PHONY venv:  # Build a virtual environment with all required packages.
venv:
	if [ ! -d ${VENV} ]; then \
  		printf "\033[0;36m\n\n--------Building venv--------\n\n\n"; \
		python3.8 -m venv $(VENV); \
		source $(VENV)/bin/activate; \
		python3.8 -m pip install pip setuptools --upgrade; \
		while read -r line; do pip install $$line; done < $(DEPENDENCIES_FILE); \
		printf "\033[0;36m\n\n--------Finished building venv--------\n\n\n"; \
	else \
		printf "\033[0;36m\n\n--------Venv already exists, if incorrect please use 'make clean-venv' and try again--------\n\n\n"; \
	fi

.PHONY dist:  # Build a deb package
dist:
	printf "\033[0;36m\n\n--------Building deb package--------\n\n\n"
	python3 setup.py --command-packages=stdeb.command bdist_deb
	printf "\033[0;36m\n\n--------Finished building the deb package--------\n\n\n"

.PHONY dist-signed:
dist-signed:
	printf "\033[0;36m\n\n--------Building and signing deb package--------\n\n\n"
	python3 setup.py --command-packages=stdeb.command sdist_dsc --sign-results bdist_deb
	printf "\033[0;36m\n\n--------Finished building and signing the deb package--------\n\n\n"


.PHONY install:  # Install the deb package
install: dist
	printf "\033[0;36m\n\n--------Installing deb package--------\n\n\n"
	dpkg -i deb_dist/*.deb || true  # ignore the error of missing dependencies
	apt-get -f install              # as we are installing them via this command
	printf "\033[0;36m\n\n--------Finished installing the deb package--------\n\n\n"

.PHONY uninstall:  # Uninstall the deb package
uninstall:
	apt remove $(DEB_PACKAGE_NAME)

.PHONY launch:
launch: venv  # Source the venv and launch the app.
	printf "\033[0;36m\n\n--------Launching dev build--------\n\n\n"; \
	source $(VENV)/bin/activate; \
	python3 setup.py install; \
	python3 -m eyecare_reminder.main; \
