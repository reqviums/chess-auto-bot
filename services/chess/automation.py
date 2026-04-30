from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import random

from core.config import Config
from core.state import AppState, ProgramState
from services.chess.utility import chess_timer_to_seconds, parse_castling, to_chess_notation, parse_promotion, extract_square, switch_side
from core.windows_utility import get_default_title_bar_height
from core.chrome import switch_to_tab_by_url, open_chrome_driver_when_ready, launch_chrome
from core.human_behavior import human_drag, rand_delay

def is_game_over(driver: WebDriver, my_side: str, online_side_to_move: str):
    try:
        driver.find_element(By.CSS_SELECTOR, '[data-cy="game-over-header"]')

        if my_side == online_side_to_move:
            print("[-] Game is over. You WON")
        else:
            print("[-] Game is over. You LOST")
            
        return True
    except NoSuchElementException:
        pass
    return False

def get_remaining_time(online_driver: WebDriver, my_side: str):
    try:
        if my_side == Config.SIDE_WHITE:
            clock_element = online_driver.find_element(
                By.CSS_SELECTOR,
                ".clock-component.clock-white .clock-time-monospace")
        elif my_side == Config.SIDE_BLACK:
            clock_element = online_driver.find_element(
                By.CSS_SELECTOR,
                ".clock-component.clock-black .clock-time-monospace")
            pass
        else:
            raise("Unknown side")
        
        seconds = chess_timer_to_seconds(clock_element.text)
    except Exception:
        return -1
    return seconds

def wait_for_next_move(driver: WebDriver, last_move_amount, side_to_move, my_side, state: AppState):
    while True:
        if is_game_over(driver, state.game.my_side, state.game.online_side_to_move):
            state.game.state = ProgramState.GAME_OVER
            if Config.ENABLE_SPEAKER:
                    state.system.speaker_engine.say("Game over")
                    state.system.speaker_engine.runAndWait()
            break

        try:
            move_elements = driver.find_elements(
                By.CSS_SELECTOR, "wc-simple-move-list span.node-highlight-content")
            current_move = move_elements[-1].text.strip()
            current_move_amount = len(move_elements)
        except Exception:
            continue

        highlight_elements = driver.find_elements(By.CSS_SELECTOR, "wc-chess-board .highlight")
        highlight_squares = []
        while True:
            if is_game_over(driver, state.game.my_side, state.game.online_side_to_move):
                state.game.state = ProgramState.GAME_OVER
                if Config.ENABLE_SPEAKER:
                    state.system.speaker_engine.say("Game over")
                    state.system.speaker_engine.runAndWait()
                break

            for e in highlight_elements:
                cls = e.get_attribute("class")
                match = re.search(r"square-(\d+)", cls)
                if match:
                    highlight_squares.append(match.group(1))

            highlight_squares = list(dict.fromkeys(highlight_squares))

            if len(highlight_squares) == 2:
                break

            time.sleep(0.05)

        try:
            (hx1, hy1), (hx2, hy2) = highlight_squares
        except Exception:
            break

        first_highlight = to_chess_notation(int(hx1), int(hy1))
        second_highlight = to_chess_notation(int(hx2), int(hy2))

        if current_move_amount == last_move_amount:
            continue

        if side_to_move == my_side:
            side_to_move = switch_side(side_to_move)
            last_move_amount = current_move_amount
            continue

        started_from = None
        extracted_square = None
        castling_result = parse_castling(current_move, side_to_move)
        extracted_square, promoted_piece = parse_promotion(current_move)
        if castling_result:
            started_from, current_move = castling_result
            extracted_square = extract_square(current_move)
            print("[-] (" + driver.capabilities["goog:chromeOptions"]["debuggerAddress"] + ") Castling "
                + started_from + " -> " + extracted_square)
        else:
            extracted_square = extract_square(current_move)
            if first_highlight == extracted_square:
                started_from = second_highlight
            elif second_highlight == extracted_square:
                started_from = first_highlight
            else:
                print(f"[E] highlight mismatch | move={current_move} -> {extracted_square} | highlights={[first_highlight, second_highlight]}")

        print("[-] (" + driver.capabilities["goog:chromeOptions"]["debuggerAddress"] + ") "
                + started_from + " -> " + extracted_square)
        side_to_move = switch_side(side_to_move)
        last_move_amount = current_move_amount

        return (started_from, extracted_square, last_move_amount, side_to_move, promoted_piece)
    return (None, None, None, None, None)

def try_promote_piece(promoted_piece: str, to_display_posX, to_display_posY):
    if promoted_piece is not None:
        promoted_y_offset = None
        if promoted_piece == 'q': # promoted queen
            promoted_y_offset = 0
        elif promoted_piece == 'n':
            promoted_y_offset = Config.SQUARE_SIZE
        elif promoted_piece == 'r':
            promoted_y_offset = Config.SQUARE_SIZE * 2
        elif promoted_piece == 'b':
            promoted_y_offset = Config.SQUARE_SIZE * 3
        else:
            print(f"[E] Unknown promotion piece: {promoted_piece}. Falling back to queen")
            promoted_y_offset = 0 # fallback to queen so the code doesnt cry and crash 

        human_drag((to_display_posX,
                to_display_posY),
                (to_display_posX,
                to_display_posY - promoted_y_offset))

def simulate_thinking(remaining_time: int, opponent_move_time: int, online_move_amount: int):
    slow_move_chance = random.random() # probability that the bot will take a slower-than-usual decision step

    if online_move_amount <= 5: # quick first steps
        rand_delay(0, 2)

    elif opponent_move_time <= 10: # opponent moved quickly -> we "think" longer
        if remaining_time >= 300: # 5 minutes
            if slow_move_chance < 0.3: # slow move
                rand_delay(5, 25)
            else:
                rand_delay(2, 5)
        elif remaining_time >= 150: # 2.3 minutes
            if slow_move_chance < 0.2: # slow move
                rand_delay(5, 20)
            else:
                rand_delay(1, 5)
        elif remaining_time >= 60: # 1 minute
            if slow_move_chance < 0.1: # slow move
                rand_delay(5, 15)
            else:
                rand_delay(1, 4)
        else:
            rand_delay(0, 1)

    elif opponent_move_time <= 30: # average thinking time -> normal delay
        if remaining_time >= 300: # 5 minutes
            if slow_move_chance < 0.4: # slow move
                rand_delay(5, 15)
            else:
                rand_delay(1, 5)
        elif remaining_time >= 150: # 2.3 minutes
            if slow_move_chance < 0.3: # slow move
                rand_delay(5, 10)
            else:
                rand_delay(1, 7)
        elif remaining_time >= 60: # 1 minute
            if slow_move_chance < 0.1: # slow move
                rand_delay(1, 5)
            else:
                rand_delay(0, 3)
        else:
            rand_delay(0, 1)

    elif opponent_move_time <= 60: # opponent spent some time -> we respond a bit faster
        if remaining_time >= 300: # 5 minutes
            if slow_move_chance < 0.4: # slow move
                rand_delay(10, 35)
            else:
                rand_delay(2, 6)
        elif remaining_time >= 150: # 2.3 minutes
            if slow_move_chance < 0.4: # slow move
                rand_delay(6, 20)
            else:
                rand_delay(2, 4)
        elif remaining_time >= 60: # 1 minute
            if slow_move_chance < 0.1: # slow move
                rand_delay(1, 4)
            else:
                rand_delay(0, 3)
        else:
            rand_delay(0, 1)

    else: # opponent took a long time → fast response (as if we pre-calculated)
        if remaining_time >= 300: # 5 minutes
            if slow_move_chance < 0.1: # slow move
                rand_delay(20, 50)
            else:
                rand_delay(3, 6)
        elif remaining_time >= 150: # 2.3 minutes
            if slow_move_chance < 0.1: # slow move
                rand_delay(10, 25)
            else:
                rand_delay(2, 7)
        elif remaining_time >= 60: # 1 minute
            if slow_move_chance < 0.25: # slow move
                rand_delay(7, 20)
            else:
                rand_delay(1, 4)
        else:
            rand_delay(0, 1)

def open_chess_session(port, user_data_dir, url):
    launch_chrome(port, user_data_dir, url)
    driver = open_chrome_driver_when_ready(f"{Config.LOCALHOST}:{port}")
    switch_to_tab_by_url(driver, url)
    if Config.USE_DUMMY_DRIVER_WAIT:
        time.sleep(Config.DUMMY_DRIVER_DELAY)
    else:
        WebDriverWait(driver, Config.CHROME_LAUNCH_TIMEOUT).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
        )
        WebDriverWait(driver, Config.CHROME_LAUNCH_TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "wc-chess-board"))
        )
    return driver

def find_and_apply_online_coords(state: AppState):
    element = state.system.online_driver.find_element(By.CSS_SELECTOR, "wc-chess-board")

    rect = state.system.online_driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {x: r.x, y: r.y, width: r.width, height: r.height};
    """, element)

    window_pos = state.system.online_driver.get_window_position()

    inner_width = state.system.online_driver.execute_script("return window.innerWidth")
    outer_width = state.system.online_driver.execute_script("return window.outerWidth")

    state.board.online_square_size = rect["width"] // Config.BOARD_SIZE
    state.board.online_square_half_size = state.board.online_square_size // 2
    state.board.online_board_origin_x = int(rect['x'] + window_pos['x']) + ((outer_width - inner_width) // 2)
    state.board.online_board_origin_y = int(rect['y'] + window_pos['y']) + get_default_title_bar_height()

def find_and_apply_bot_coords(state: AppState): 
    element = state.system.bot_driver.find_element(By.CSS_SELECTOR, "wc-chess-board")

    rect = state.system.bot_driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {x: r.x, y: r.y, width: r.width, height: r.height};
    """, element)

    window_pos = state.system.bot_driver.get_window_position()

    inner_width = state.system.bot_driver.execute_script("return window.innerWidth")
    outer_width = state.system.bot_driver.execute_script("return window.outerWidth")

    state.board.bot_square_size = rect["width"] // Config.BOARD_SIZE
    state.board.bot_square_half_size = state.board.bot_square_size // 2
    state.board.bot_board_origin_x = int(rect['x'] + window_pos['x']) + ((outer_width - inner_width) // 2)
    state.board.bot_board_origin_y = int(rect['y'] + window_pos['y']) + get_default_title_bar_height()