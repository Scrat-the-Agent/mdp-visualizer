from PyQt5.QtCore import QEasingCurve, QPropertyAnimation

def animate(obj, prop, time, val):
    anim = QPropertyAnimation(obj, prop.encode())
    anim.setEasingCurve(QEasingCurve.InQuad)
    anim.setDuration(time)
    anim.setEndValue(val)
    anim.start()

    return anim

def value_update(value, target_value):
    '''
    By current value and target value returns value after one animation step (float)
    '''
    diff = abs(target_value - value)
    step = max(0.1, diff / 20)

    if diff < step:
        return target_value, True
    elif target_value > value:
        return value + step, False
    else:
        return value - step, False
