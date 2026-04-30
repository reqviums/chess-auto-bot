class Config:
    # =====================================================
    # SYSTEM CONFIG
    # =====================================================
    BASE_DIR = __file__.rsplit("\\", 1)[0]
    
    SIDE_WHITE = 'white'
    SIDE_BLACK = 'black'

    BOARD_SIZE = 8

    LOCALHOST = "127.0.0.1"

    ONLINE_PORT = 9225
    BOT_PORT = 9226

    ONLINE_CHESS_LINK = "https://www.chess.com/play/online"
    BOT_CHESS_LINK = "https://www.chess.com/play/computer"

    CHROME_LAUNCH_TIMEOUT = 10  # max time (seconds) to wait for Chrome debugging endpoint

    USE_DUMMY_DRIVER_WAIT = False  # use simplified wait (sleep) instead of strict WebDriverWait; enable only if Chrome/page loading becomes unstable
    DUMMY_DRIVER_DELAY = 2


    

    # =====================================================
    # USER CONFIG 
    # =====================================================

    # directories
    # -----------------------------------------------------  
    CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # Path to Chrome executable (change if installed elsewhere)

    ONLINE_PROFILE_DIR = BASE_DIR + r"\online_profile"  # Chrome user profile for online play session
    BOT_PROFILE_DIR = BASE_DIR + r"\bot_profile"  # Chrome user profile for bot (computer play) session  


    # hotkeys
    # -----------------------------------------------------    
    START_BOT_KEY = "w" # start bot hotkey
    QUIT_KEY = "q" # key to stop the program


    # utility
    # -----------------------------------------------------
    ENABLE_SPEAKER = True # enable voice notifications (TTS)


    # delay
    # -----------------------------------------------------    
    NEXT_GAME_DELAY_RANGE = (5, 10) # delay range before next game search
    UI_GAME_START_ANIMATION_DELAY = 0.5  # allow UI animation to settle before next action
    

    # mouse simulation
    # -----------------------------------------------------    
    MOUSE_BASE_MOVE_DURATION_RANGE = (0.15, 0.4)   # base movement speed
    MOUSE_DRAG_DURATION_RANGE = (0.3, 0.6)         # drag final segment speed
    MOUSE_MIDPOINT_DURATION_RANGE = (0.1, 0.2)     # midpoint movement speed

    HUMAN_DRAG_MIDPOINT_CHANCE = 0.5               # chance to use curved drag
    HUMAN_DRAG_MIDPOINT_OFFSET = 20                # randomness of mid point

    MOUSE_CLICK_DOWN_UP_DELAY_RANGE = (0.03, 0.1)  # click realism delay

    RAND_OFFSET_PIXELS = 3                         # small human hand jitter