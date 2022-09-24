import os
from xdg import BaseDirectory

# config defaults
default_reminder_interval = 1200  # seconds - 1200 is 20 minutes
default_reminder_cooldown_interval = 120  # seconds to look in the distance for
default_idle_time = 300  # seconds - 300 is 5 minutes
default_suppress_when_microphone_active = True
default_enable_sound = True
default_blacklist_process_names = []
default_blacklist_window_names = []

# config location
default_config_location = os.path.join(
    BaseDirectory.xdg_config_home, "eyecare_reminder", "config.yaml"
)

# log location
default_log_location = os.path.join(
    BaseDirectory.xdg_config_home, "eyecare_reminder", "log.log"
)

# messages
reminder_message = "Look in the distance for {} seconds."
reminder_end_message = "You can go back to whatever you were doing now."
config_reloaded_message = "Config successfully reloaded"
next_reminder_message = "Next reminder at: {}"

# sounds
reminder_sound = os.path.abspath(
    os.path.join(__file__, "..", "sounds", "relax-message-tone.wav")
)
cooldown_sound = os.path.abspath(
    os.path.join(__file__, "..", "sounds", "piece-of-cake-611.wav")
)

# icon
icon = os.path.join(__file__, "..", "images", "icon.png")
icon_attention = os.path.join(__file__, "..", "images", "icon_attention.png")
icon_animation_speed = 500

# notification
reminder_notification_duration = 10000
reminder_cooldown_duration = 10000

# desktop file
desktop_file_name = "eyecare_reminder.desktop"
desktop_file_icon_path = os.path.abspath(
    os.path.join(
        BaseDirectory.xdg_data_home, "icons", "eyecare_reminder", "icon.png",
    )
)
autostart_key = "X-GNOME-Autostart-enabled"
icon_key = "Icon"


class ConfigKey(object):

    def __init__(self, name, _type, default_value):
        """Config key object storing key name and value type."""
        self.name = name
        self.type = _type
        self.default_value = default_value


class ConfigKeys(object):
    """Initialize and store the config key objects for later reference."""
    reminder_interval = ConfigKey("reminder_interval", int, default_reminder_interval)
    reminder_cooldown_interval = ConfigKey("reminder_cooldown_interval", int, default_reminder_cooldown_interval)
    idle_time = ConfigKey("idle_time", int, default_idle_time)
    suppress_when_microphone_active = ConfigKey("suppress_when_microphone_active", bool, default_suppress_when_microphone_active)
    enable_sound = ConfigKey("enable_sound", bool, default_enable_sound)
    blacklist_process_names = ConfigKey("blacklist_process_names", list, default_blacklist_process_names)
    blacklist_window_names = ConfigKey("blacklist_window_names", list, default_blacklist_window_names)


def configKeysAsList():
    """Return the config key objects as a list.

    Returns:
        list[ConfigKey]: The config key objects as a list.
    """
    return [
        ConfigKeys.reminder_interval,
        ConfigKeys.reminder_cooldown_interval,
        ConfigKeys.idle_time,
        ConfigKeys.suppress_when_microphone_active,
        ConfigKeys.enable_sound,
        ConfigKeys.blacklist_window_names,
        ConfigKeys.blacklist_process_names,
    ]
