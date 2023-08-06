"""
Utility functions
"""
from .conf import nlf_settings


def coerce_bool(value):
    """Coerces any value to a boolean. String values are checked for the first letter
    and matched against the `FALSE_VALUES` setting.
    """
    if isinstance(value, str) and len(value) > 0:
        return value[0].lower() not in nlf_settings.FALSE_VALUES
    return bool(value)


def camel_to_snake_case(value: str) -> str:
    """Converts strings in camelCase to snake_case.

    :param str value: camalCase value.
    :return: snake_case value.
    :rtype: str
    """
    return "".join(["_" + char.lower() if char.isupper() else char for char in value]).lstrip("_")
