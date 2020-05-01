from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QColor, QFont
import gettext

from .utils import path

# LOCALISATION AND TEXTS -------------------------------------------------------

ru = gettext.translation('game', path('locale'), languages=['ru'])
ru.install()

I_AM_RL_AGENT = _("I Am RL Agent")
AUTOMATIC_RL = _("Automatic RL, Please")
Q_LEARNING_DESCRIPTION = _("Press play to launch\nQ-learning algorithm!\n\nHover over cells to watch\nQ-values for them.\n")
IAMRLAGENT_DESCRIPTION = _("Select one of 6 possible actions.\n\nLearn how to get as much \nreward per episode as possible!\n")

EPISODE_END_MESSAGE = _("Episode has finished!\nPress reset to start a new one!")
INFO_BOX = _("Press T to rotate the game view!")

# IMAGES -----------------------------------------------------------------------


BACKGROUND_IMAGE = path("images/blue_angle_swirl.jpg")
REWARD_FRAME_IMAGE = path("images/frame.png")
REWARD_ICON_IMAGE = path("images/nut")

SCRAT_IMAGE = path("images/scrat_drawing2.png")
SCRAT_AND_WATERMELON_IMAGE = path("images/scrat_drawing2_and_watermelon.png")
SCRAT_WITH_WATERMELON_IMAGE = path("images/scrat_drawing2_with_watermelon.png")
SCRAT_HIPPO_IMAGE = path("images/scrat_hippo.png")
SCRAT_HIPPO_AND_WATERMELON_IMAGE = path("images/scrat_hippo_and_watermelon.png")
SCRAT_WITH_WATERMELON_HIPPO_IMAGE = path("images/scrat_with_watermelon_hippo.png")
SCRAT_HIPPO_FED_IMAGE = path("images/scrat_hippo_fed.png")
HIPPO_IMAGE = path("images/hippo_drawing_mirrored.png")
HIPPO_AND_WATERMELON_IMAGE = path("images/hippo_drawing_mirrored_and_watermelon.png")
WATERMELON_IMAGE = path("images/watermelon_drawing_small_rotated.png")
LAVA_IMAGE = path("images/lava_drawing.png")

PLAY_BUTTON_IMAGE = path("images/play")
STEP_BUTTON_IMAGE = path("images/step")
RESET_BUTTON_IMAGE = path("images/repeat")
FULL_RESET_BUTTON_IMAGE = path("images/newgame")
STOP_BUTTON_IMAGE = path("images/stop")
INFO_IMAGE = path("images/info")
INFO_CLOSE_IMAGE = path("images/infopressed")

RIGHT_ARROW_BUTTON_IMAGE = path("images/right")
LEFT_ARROW_BUTTON_IMAGE = path("images/left")
DOWN_ARROW_BUTTON_IMAGE = path("images/down")
UP_ARROW_BUTTON_IMAGE = path("images/up")

BUTTONS_PATHS = [
    path("images/symbol" + str(i))
    for i in range(6)
]

# ANIMATION TIME ---------------------------------------------------------------

MOVE_TIME = 300
ROTATION_TIME = 600
MODE_SWITCH_TIME = 400
Q_LEARNING_PLAY_SPEED = 500

VALUE_UPDATE_TIME = 15
VALUE_UPDATE_MAX_STEPS = 20

# ROTATION CONFIGURATION -------------------------------------------------------

ROTATION_ANGLE = 55
SCALE_WHEN_ROTATED = 0.75
BASE_CELL_OPACITY = 0.65

# GAME LOGIC PARAMETERS --------------------------------------------------------

GAME_HEIGHT = 4
GAME_WIDTH = 5

# IAmRLAgent mode
IAMRLAGENT_LAVA_RANDOM = 5
HIPPO_MOVE_PROB = 0.3
WATERMELON_MOVE_PROB = 0.1
TICK_PENALTY = -0.1

# AutomaticRL mode
AUTOMATIC_LAVA_RANDOM = 5
GREEN_RANDOM = 2

LAVA_REWARD = -10.0
GREEN_REWARD = 10.0
MIN_REWARD = -10
MAX_REWARD = +10

MAX_FLOAT_DIFF = 1e-6

# COLOR AND DESIGN -------------------------------------------------------------

PAD_COLOR = QColor(226, 255, 92, 64)
SELECTION_COLOR = QColor(Qt.gray)
ICON_COLOR = QColor(80, 90, 100, 255)
ICON_RECT = QRectF(-54, -54, 108, 108)

RED_CELL = QColor(200, 10, 10, 255)
YELLOW_CELL = QColor(200, 200, 10, 255)
GREEN_CELL = QColor(10, 200, 10, 255)

REWARD_COLOR = QColor(0, 0, 0, 255)
REWARD_FONT = QFont("Impact", weight=QFont.Bold)
REWARD_FONT.setPixelSize(36)

# GEOMETRY. NAILS -------------------------------------------------------------

LEFT_SCREEN_NAILS_WIDTH = 350
BUTTONS_NAILS_WIDTH = 200
Q_VISUALIZATION_NAILS = QSize(300, 250)
AUTO_RL_DESCRIPTION_NAILS = QSize(300, 250)
IAMRLAGENT_DESCRIPTION_NAILS = QSize(300, 175)
REWARD_LABEL_NAILS = QSize(225, 150)
INFO_SIZE_NAIL = 80
INFO_MARGIN_NAIL = 100