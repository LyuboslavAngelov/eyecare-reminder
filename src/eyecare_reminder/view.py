from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QMessageBox, QAction
from PyQt5.QtGui import QIcon


from . import config, utils


class View(QSystemTrayIcon):

    def __init__(self, controller):
        """Initialize the view object.

        Args:
            controller (eyecare_reminder.eyecare_reminder.EyecareReminder):
                The controller object.
        """
        self._controller = controller
        self.checkTray()
        super().__init__()

        self.icon_default = QIcon(config.icon)
        self.icon_attention = QIcon(config.icon_attention)
        self.setIcon(self.icon_default)
        self.current_icon_file = config.icon

        self.edit_config_action = QAction("Edit config")
        self.reload_config_action = QAction("Reload config")
        self.open_log_action = QAction("Open log")
        self.reset_to_default_action = QAction("Reset to default")
        self.exit_action = QAction("Exit")

        self.autostart_action = QAction("Autostart")
        self.autostart_action.setCheckable(True)
        if config.system == "Linux":
            autostart = self._controller.getDesktopFileAutostart()
            if autostart:
                self.autostart_action.setChecked(True)

        self.edit_config_action.triggered.connect(self._controller.editConfig)
        self.reload_config_action.triggered.connect(self._controller.reloadConfig)
        self.open_log_action.triggered.connect(self._controller.openLog)
        self.reset_to_default_action.triggered.connect(self.showResetToDefaultMessage)
        self.autostart_action.triggered.connect(self._controller.toggleAutostart)
        self.exit_action.triggered.connect(self._controller.exit)

        menu = QMenu()
        menu.addAction(self.edit_config_action)
        menu.addAction(self.reload_config_action)
        menu.addAction(self.open_log_action)
        menu.addSeparator()
        menu.addAction(self.reset_to_default_action)
        menu.addSeparator()
        menu.addAction(self.autostart_action)
        menu.addSeparator()
        menu.addAction(self.exit_action)
        self.setContextMenu(menu)

        self.setVisible(True)

    def showReminderMessage(self, play_sound=True):
        """Show the reminder message as a notification.

        Args:
            play_sound (bool): Whether to play sound or not.
        """
        self.showMessage(
            "Eyecare Reminder",
            config.reminder_message.format(self._controller.getCooldownValue()),
            self.icon_attention,
            config.reminder_notification_duration
        )
        if play_sound:
            utils.play_sound(config.reminder_sound)

    def showCooldownMessage(self, play_sound=True):
        """Show the cooldown message as a notification.

        Args:
            play_sound (bool): Whether to play sound or not.
        """
        self.showMessage(
            "Eyecare Reminder",
            config.reminder_end_message,
            self.icon_default,
            config.reminder_cooldown_duration,
        )
        if play_sound:
            utils.play_sound(config.cooldown_sound)

    def showBadConfigMessage(self):
        """Open a window asking the user whether to restore the default config.
        """
        button_reply = QMessageBox.question(
            None,
            'Broken config',
            "The config file is broken, would you like to restore defaults?",
        )
        if button_reply == QMessageBox.StandardButton.Yes:
            self._controller.writeDefaultConfig()
        else:
            self._controller.editConfig()

    def showConfigReloadedMessage(self):
        """Show the config reloaded message as a notification."""
        self.showMessage(
            "Eyecare Reminder",
            config.config_reloaded_message,
            self.icon_default,
            3000,
        )

    def showResetToDefaultMessage(self):
        """Open a window asking the user whether they want to
        restore the default config."""
        button_reply = QMessageBox.question(
            None,
            'Reset to default?',
            "Are you sure you want to restore defaults?",
        )
        if button_reply == QMessageBox.StandardButton.Yes:
            self._controller.writeDefaultConfig()

    def setReminderToolTip(self, time):
        """Set the tooltip to the time the next reminder will be at.

        Args:
            time (str): The time the next reminder will be at in HH:MM format.
        """
        self.setToolTip(config.next_reminder_message.format(time))

    def setDefaultTrayIcon(self):
        """Set the default tray icon."""
        self.setIcon(self.icon_default)
        self.current_icon_file = config.icon

    def setAttentionTrayIcon(self):
        """Set the attention tray icon."""
        self.setIcon(self.icon_attention)
        self.current_icon_file = config.icon_attention

    def animateIcon(self):
        """Animate the tray icon. Switch between default and attention icon.

        Returns:
            bool: Whether animation is playing correctly or not.
        """
        if self.current_icon_file == config.icon:
            self.setAttentionTrayIcon()
        elif self.current_icon_file == config.icon_attention:
            self.setDefaultTrayIcon()
        else:
            return False
        return True

    def checkTray(self):
        """Perform checks whether tray is available and whether messages are
        supported.

        Notify user and quit if either is unsupported.
        """
        if not self.isSystemTrayAvailable() or not self.supportsMessages():
            QMessageBox.critical(
                None,
                "Critical Error",
                "System tray missing or messages unsupported on platform."
                "\n\nExiting."
            )
            self._controller.exit()
