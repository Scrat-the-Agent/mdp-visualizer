from PyQt5.QtCore import QEasingCurve, QPropertyAnimation

def animate(obj, prop, time, val):
    anim = QPropertyAnimation(obj, prop.encode())
    anim.setEasingCurve(QEasingCurve.InQuad)
    anim.setDuration(time)
    anim.setEndValue(val)
    anim.start()

    return anim
