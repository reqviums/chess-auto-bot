from enum import Enum
from core.config import Config

class ProgramState(Enum):
    SEARCHING_GAME = 1
    SETUP = 2
    AUTO_BOT = 3
    GAME_OVER = 4

class SystemState:
    def __init__(self):
        self.speaker_engine = None
        self.online_driver = None
        self.bot_driver = None
        self.is_running = True

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = ProgramState.SEARCHING_GAME
        self.my_side = None
        self.online_last_move_amount = 0
        self.bot_last_move_amount = 0
        self.online_side_to_move = Config.SIDE_WHITE
        self.bot_side_to_move = Config.SIDE_WHITE
        self.opponent_move_time = 0
        self.online_move_amount = 0

class BoardState:
    def __init__(self):
        self.online_board_origin_x = None
        self.online_board_origin_y = None

        self.bot_board_origin_x = None
        self.bot_board_origin_y = None

        self.online_square_size = None
        self.online_square_half_size = None

        self.bot_square_size = None
        self.bot_square_half_size = None

class AppState:
    def __init__(self):
        self.system = SystemState()
        self.game = GameState()
        self.board = BoardState()