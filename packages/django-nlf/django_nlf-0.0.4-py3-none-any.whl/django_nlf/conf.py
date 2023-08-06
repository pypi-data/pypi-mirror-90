"""
Configuration module
"""
import warnings

from django.conf import settings as dj_settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None

    if isinstance(val, str):
        return import_from_string(val, setting_name)

    if isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]

    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = "Could not import '%s' for NLF setting '%s'. %s: %s." % (
            val,
            setting_name,
            e.__class__.__name__,
            e,
        )
        raise ImportError(msg) from e


def deprecate(msg, level_modifier=0):
    warnings.warn(msg, DeprecationWarning, stacklevel=3 + level_modifier)


class NLFSettings:
    DEFAULTS = {
        "EMPTY_VALUE": "EMPTY",
        "FALSE_VALUES": ("0", "f"),
        "FIELD_NAME_CONVERTER": None,
        "FIELD_SHORTCUTS": {},
        "PATH_SEPARATOR": ".",
        "QUERY_PARAM": "q",
    }

    DEPRECATED_SETTINGS = []

    # List of settings that may be in string import notation.
    IMPORT_STRINGS = ["FIELD_NAME_CONVERTER"]

    def __getattr__(self, name):
        if name not in self.DEFAULTS:
            msg = "'%s' object has no attribute '%s'"
            raise AttributeError(msg % (self.__class__.__name__, name))

        value = self.get_setting(name)

        # Cache the result
        setattr(self, name, value)
        return value

    def get_setting(self, setting):
        django_setting = f"NLF_{setting}"

        if setting in self.DEPRECATED_SETTINGS:
            deprecate(f"The '{django_setting}' setting has been deprecated.")

        val = getattr(dj_settings, django_setting, self.DEFAULTS[setting])

        if setting in self.IMPORT_STRINGS:
            val = perform_import(val, setting)

        return val

    def change_setting(self, setting, value, enter, **kwargs):
        if not setting.startswith("NLF_"):
            return
        setting = setting[4:]  # strip 'NLF_'

        # if existing, delete value to repopulate
        if hasattr(self, setting):
            delattr(self, setting)


nlf_settings = NLFSettings()
setting_changed.connect(nlf_settings.change_setting)
