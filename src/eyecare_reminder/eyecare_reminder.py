import ast
import logging
import os
import subprocess
import time

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QApplication
from xdg import BaseDirectory, DesktopEntry

from .config import ConfigKeys
from . import config, utils

if not os.path.exists(config.default_log_location):
    utils.createLogFile()
logging.basicConfig(
    filename=config.default_log_location,
    filemode="a",
    format="%(asctime)s[%(name)s][%(levelname)s] %(message)s",
    datefmt="[%Y-%m-%d][%H:%M:%S]",
    level=logging.DEBUG,
    force=True,
)

_LOGGER = logging.getLogger(__name__)


class EyecareReminder(QObject):

    def __init__(self):
        """Initialize the Eyecare controller."""
        super().__init__()
        self._view = None
        self._config = {}
        self._timer = QTimer()
        self._timer_animation = QTimer()
        self._timer.timeout.connect(self._timeout)
        self._timer_animation.timeout.connect(self._timeoutAnimation)
        if config.system == "Linux":
            self.setDesktopFileIconPath()
        _LOGGER.info("STARTING")

    def setup(self, view):
        """Set up the controller.

        Adds reference to the view object and imports the config.

        Args:
            view (eyecare-reminder.view.View): The view object.
        """
        self._view = view
        self.reloadConfig()

    def _startReminderTimer(self):
        """Start the reminder timer."""
        _LOGGER.info("STARTED REMINDER TIMER")
        interval = self._config.get(ConfigKeys.reminder_interval.name)
        interval = utils.convert_seconds_to_ms(interval)
        self._view.setReminderToolTip(self._getNextTimeoutTime())
        self._timer.start(interval)
        self._timer_animation.stop()
        self._view.setDefaultTrayIcon()

    def _startReminderCooldownTimer(self):
        """Start the cooldown timer."""
        _LOGGER.info("STARTED COOLDOWN TIMER")
        interval = self._config.get(ConfigKeys.reminder_cooldown_interval.name)
        interval = utils.convert_seconds_to_ms(interval)
        self._timer.start(interval)
        self._timer_animation.start(config.icon_animation_speed)

    def _timeout(self):
        """Timeout callback method.

        Validates the timeout, shows correct message and starts correct timer.
        """
        is_valid_timeout = self._validateTimeout()
        interval = utils.convert_ms_to_seconds(self._timer.interval())

        reminder_interval_key = ConfigKeys.reminder_interval.name
        reminder_cooldown_key = ConfigKeys.reminder_cooldown_interval.name
        enable_sound = self._config.get(ConfigKeys.enable_sound.name)

        if interval == self._config.get(reminder_interval_key):
            if is_valid_timeout:
                self._view.showReminderMessage(play_sound=enable_sound)
                self._startReminderCooldownTimer()
            else:
                self._startReminderTimer()
        elif interval == self._config.get(reminder_cooldown_key):
            if is_valid_timeout:
                self._view.showCooldownMessage(play_sound=enable_sound)
            self._startReminderTimer()

    def _timeoutAnimation(self):
        """Timeout callback for animation.

        Changes the system tray icon.
        """
        success = self._view.animateIcon()
        if not success:
            _LOGGER.error("Could not switch icon")

    def _getNextTimeoutTime(self):
        """Return the time the next reminder will be at.

        Returns:
            str: Time next reminder will be at in HH:MM format
        """
        interval_time = self._config.get(ConfigKeys.reminder_interval.name)
        next_time = time.time() + interval_time
        return time.strftime("%H:%M", time.localtime(next_time))

    def _validateTimeout(self):
        """Check whether the timeout is valid.

        Timeout can be invalid if microphone is in use, the system is idle
        or a blacklisted application is running.

        Returns:
            bool: Whether the timeout is valid or not.
        """
        mic_key_name = ConfigKeys.suppress_when_microphone_active.name
        if self._isSystemIdle():
            return False
        elif self._config.get(mic_key_name) and self._isMicrophoneActive():
            return False
        elif self._isBlacklistedWindowRunning():
            return False
        else:
            return True

    def _isSystemIdle(self):
        """Check whether the system is idle.

        Returns:
            bool: Whether the system is idle.
        """
        key = ConfigKeys.idle_time.name
        idle_time = utils.convert_seconds_to_ms(self._config.get(key))
        output = subprocess.check_output(["xprintidle"])
        if int(output.decode()) >= idle_time:
            _LOGGER.info("SYSTEM IDLE")
            return True
        else:
            return False

    @staticmethod
    def _isMicrophoneActive():
        """Check whether the microphone is currently active.

        Returns:
            bool: Whether the microphone is currently active.
        """
        output = subprocess.check_output(
            ["pacmd", "list-sources", "|", "grep", "RUNNING"]
        )
        if "state: RUNNING" in str(output):
            _LOGGER.info("MICROPHONE ACTIVE")
            return True
        else:
            return False

    def _isBlacklistedProcessRunning(self):
        """Check whether a blacklisted process is currently running.

        Returns:
            bool: Whether a blacklisted process is currently running.
        """
        key_name = ConfigKeys.blacklist_process_names.name
        for process_name in self._config.get(key_name):
            if utils.checkIfProcessRunning(process_name):
                _LOGGER.info(
                    "BLACKLISTED PROCESS RUNNING: {}".format(process_name)
                )
                return True
        return False

    def _isBlacklistedWindowRunning(self):
        """Check whether a blacklisted window is currently open.

        Returns:
            bool: Whether a blacklisted window is currently open.
        """
        output = subprocess.check_output(["xwininfo", "-tree", "-root"])
        key_name = ConfigKeys.blacklist_window_names.name
        for window_name in self._config.get(key_name):
            if utils.checkIfWindowRunning(window_name, output=output):
                _LOGGER.info(
                    "BLACKLISTED WINDOW RUNNING: {}".format(window_name)
                )
                return True
        return False

    def writeDefaultConfig(self):
        """Write a default config at the default config location specified in
        eyecare_reminder.config"""
        data = {}
        for key in config.configKeysAsList():
            data[key.name] = key.default_value
        utils.write_yaml(config.default_config_location, data)
        _LOGGER.info("CONFIG RESET TO DEFAULT")
        self.reloadConfig()

    def importConfig(self):
        """Import a config from the default config location specified in
        eyecare_reminder.config"""
        if not os.path.exists(config.default_config_location):
            self.writeDefaultConfig()
        self._config = utils.import_yaml(config.default_config_location)

    def reloadConfig(self):
        """Reload a config from the default config location specified in
        eyecare_reminder.config"""
        self.importConfig()
        if self._validateConfig():
            self._timer.stop()
            self._startReminderTimer()
            self._view.showConfigReloadedMessage()
        else:
            self._view.showBadConfigMessage()
        _LOGGER.info("CONFIG RELOADED")

    def _validateConfig(self):
        """Validate a loaded config.

        Returns:
            bool: Whether the config is valid or not.
        """
        for key in config.configKeysAsList():
            config_val = self._config.get(key.name)
            if config_val is None or not isinstance(config_val, key.type):
                _LOGGER.error("INVALID CONFIG")
                return False
        return True

    @staticmethod
    def editConfig():
        """Open the config with the default system application for editing."""
        _LOGGER.info("EDITING CONFIG")
        subprocess.run(("xdg-open", config.default_config_location))

    @staticmethod
    def openLog():
        """Open the log file with the default system application for editing.
        """
        subprocess.run(("xdg-open", config.default_log_location))

    def getCooldownValue(self):
        """Return the current configured cooldown value.

        Returns:
            int: The currently configured cooldown value.
        """
        return self._config.get(ConfigKeys.reminder_cooldown_interval.name)

    @staticmethod
    def getDesktopFilePath():
        """Get the desktop file path.

        Returns:
            str: The desktop file path.
        """
        desktop_file = os.path.join(
            BaseDirectory.xdg_data_home,
            "applications",
            config.desktop_file_name,
        )
        if not os.path.exists(desktop_file):
            raise IOError("Installed eyecare reminder desktop file not found!")
        return desktop_file

    def readDesktopFile(self, desktop_file_path=None):
        """Open the desktop file and return it.

        Args:
            desktop_file_path (str, optional):
                Optionally supply a desktop file path.

        Returns:
            xdg.DesktopEntry.DesktopEntry: The opened desktop file.
        """
        if not desktop_file_path:
            desktop_file_path = self.getDesktopFilePath()
        return DesktopEntry.DesktopEntry(desktop_file_path)

    def getDesktopFileAutostart(self, desktop_file=None):
        """Read the desktop file and return the value of the autostart key.

        Args:
            desktop_file (xdg.DesktopEntry.DesktopEntry, optional):
                Optionally supply an already opened desktop file.
        Returns:
            bool: Whether autostart is true or false.
        """
        if not desktop_file:
            desktop_file = self.readDesktopFile()
        return ast.literal_eval(
            desktop_file.get(config.autostart_key).capitalize()
        )

    def getDesktopFileIcon(self, desktop_file=None):
        """Read the desktop file and return the value of the icon key.

        Args:
            desktop_file (xdg.DesktopEntry.DesktopEntry, optional):
                Optionally supply an already opened desktop file.
        Returns:
            str: The icon path.
        """
        if not desktop_file:
            desktop_file = self.readDesktopFile()
        return desktop_file.get(config.icon_key)

    def toggleAutostart(self):
        """Toggle starting with system."""
        if config.system == "Linux":
            desktop_file_path = self.getDesktopFilePath()
            desktop_file = self.readDesktopFile(desktop_file_path=desktop_file_path)
            enabled = self.getDesktopFileAutostart(desktop_file=desktop_file)
            if enabled:
                print("setting to false")
                desktop_file.set(config.autostart_key, "false")
            else:
                print("setting to true")
                desktop_file.set(config.autostart_key, "true")
            desktop_file.write(desktop_file_path)

    def setDesktopFileIconPath(self):
        """Sets .desktop icon absolute path as they can't be relative"""
        desktop_file_path = self.getDesktopFilePath()
        desktop_file = self.readDesktopFile(desktop_file_path=desktop_file_path)
        current_icon_path = self.getDesktopFileIcon(desktop_file=desktop_file)
        if not current_icon_path == config.desktop_file_icon_path:
            desktop_file.set(config.icon_key, config.desktop_file_icon_path)
            desktop_file.write(desktop_file_path)

    @staticmethod
    def exit():
        """Quit the application."""
        _LOGGER.info("EXITING")
        QApplication.instance().quit()
