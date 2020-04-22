from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QFont

BACKGROUND_IMAGE = "./images/blue_angle_swirl.jpg"
SCRAT_IMAGE = "./images/scrat_drawing2.png"
SCRAT_WITH_WATERMELON_IMAGE = "./images/scrat_drawing2_with_watermelon.png"
HIPPO_IMAGE = "./images/hippo_drawing_mirrored.png"
WATERMELON_IMAGE = "./images/watermelon_drawing_small_rotated.png"
LAVA_IMAGE = "./images/lava_drawing.png"

MOVE_TIME = 300
ROTATION_TIME = 600

ROTATION_ANGLE = 55
BASE_CELL_OPACITY = 0.65

GAME_HEIGHT = 5
GAME_WIDTH = 7

PAD_COLOR = QColor(226, 255, 92, 64)
SELECTION_COLOR = QColor(Qt.gray)
ICON_COLOR = QColor(80, 90, 100, 255)
ICON_RECT = QRectF(-54, -54, 108, 108)

RED_CELL = QColor(200, 10, 10, 255)
YELLOW_CELL = QColor(200, 200, 10, 255)
GREEN_CELL = QColor(10, 200, 10, 255)
MIN_REWARD = -10
MAX_REWARD = +10

REWARD_COLOR = QColor(0, 0, 0, 255)
REWARD_FONT = QFont("Impact", weight=QFont.Bold)
REWARD_FONT.setPixelSize(36)

DESCRIPTION_FONT = QFont("Times New Roman", weight=QFont.Bold)
DESCRIPTION_FONT.setPixelSize(18)

Q_LEARNING_PLAY_SPEED = 500
PLAY_BUTTON_IMAGE = "./images/play"
STEP_BUTTON_IMAGE = "./images/step"
RESET_BUTTON_IMAGE = "./images/repeat"
FULL_RESET_BUTTON_IMAGE = "./images/newgame"
STOP_BUTTON_IMAGE = "./images/stop"

RIGHT_ARROW_BUTTON_IMAGE = "./images/right"
LEFT_ARROW_BUTTON_IMAGE = "./images/left"
DOWN_ARROW_BUTTON_IMAGE = "./images/down"
UP_ARROW_BUTTON_IMAGE = "./images/up"