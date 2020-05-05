"""Utils module"""

import os
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation

from . import settings


def animate(obj, prop, time, val):
    """
    Starts animation of some QProperty for some QObject obj

    Args:
      obj: QObject
      prop: name of property, str
      time: time of animation, int
      val: target value of property

    Important: Qt requires animation to be stored as property of some QObject class!
    Otherwise animation will not be tracked by the main loop.

    Returns: QpropertyAnimation
    """
    anim = QPropertyAnimation(obj, prop.encode())
    anim.setEasingCurve(QEasingCurve.InQuad)
    anim.setDuration(time)
    anim.setEndValue(val)
    anim.start()

    return anim


def value_update(value: float, target_value: float, min_step: float = 0.1):
    """By current value and target value returns value after one animation step (float)

    Args:
      value: current value
      target_value: target value
      min_step: minimal change of value

    Returns:
      new_value: value after one step, float
      done: flag if the animation has ended, bool
    """
    diff = abs(target_value - value)
    step = max(min_step, diff / settings.VALUE_UPDATE_MAX_STEPS)

    if diff < step:
        return target_value, True
    elif target_value > value:
        return value + step, False
    else:
        return value - step, False


def path(relative_path):
    """Returns absolute path given relative path"""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, relative_path)
