from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

BACKGROUND_IMAGE = "./images/blue_angle_swirl.jpg"
SCRAT_IMAGE = "./images/scrat_drawing2.png"

MOVE_TIME = 300
ROTATION_TIME = 600

ROTATION_ANGLE = 55
BASE_CELL_OPACITY = 0.65

PAD_COLOR = QColor(226, 255, 92, 64)
SELECTION_COLOR = QColor(Qt.gray)
ICON_COLOR = QColor(80, 90, 100, 255)

RED_CELL = QColor(200, 10, 10, 255)
YELLOW_CELL = QColor(200, 200, 10, 255)
GREEN_CELL = QColor(10, 200, 10, 255)
MIN_REWARD = -10
MAX_REWARD = +10

REWARD_COLOR = QColor(0, 0, 0, 255)
REWARD_FONT = QFont("Impact", weight=QFont.Bold)
REWARD_FONT.setPixelSize(36)

COLS = 6
ROWS = 5
REDS = {(3,4), (1,2), (4,0)}
GREENS = {(2,4)}