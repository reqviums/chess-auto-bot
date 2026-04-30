from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import time
import pyautogui
from core.config import Config
from core.state import AppState, ProgramState
from core.human_behavior import human_drag, rand_delay
from services.chess.automation import simulate_thinking, try_promote_piece, wait_for_next_move, get_remaining_time, find_and_apply_online_coords, find_and_apply_bot_coords
from services.chess.utility import chess_to_square, chess_to_square_flipped, switch_side
from services.system.lifecycle import init_system
from utility.pre_run_info import show_pre_run_info

# =========================
# BOOTSTRAP (startup sequence)
# =========================
state = AppState()
state.system.speaker_engine, state.system.online_driver, state.system.bot_driver = init_system()

show_pre_run_info()

# =====================================================
# STARTUP WAIT LOOP (manual trigger)
# =====================================================
while True: # wait loop for hotkey to start auto bot
    if keyboard.is_pressed(Config.START_BOT_KEY):
        print("[-] Auto Bot started")
        if Config.ENABLE_SPEAKER:
            state.system.speaker_engine.say("Auto Bot started")
            state.system.speaker_engine.runAndWait()
        break

# hit start game button
state.system.online_driver.find_element(By.CSS_SELECTOR, '[data-cy="new-game-index-play"]').click()
state.system.online_driver.execute_script("window.scrollTo(0, 0);") # scroll up

# =====================================================
# MAIN RUNTIME LOOP (state machine)
# =====================================================
while state.system.is_running:
    online_driver = state.system.online_driver
    bot_driver = state.system.bot_driver
    speaker_engine = state.system.speaker_engine

    if state.game.state == ProgramState.SEARCHING_GAME:
            try:
                # detect game start by UI clock elements
                clock_elements = state.system.online_driver.find_elements(By.CSS_SELECTOR, '[class="clock-time-monospace"]')
                try:
                    find_new_game_button = state.system.online_driver.find_element(By.CSS_SELECTOR, '[data-cy="game-over-modal-new-game-button"]')
                    find_new_game_button.click()
                except Exception:
                    pass

                for el in clock_elements:
                    minutes = el.text.split(":")[1]
                    if minutes != "00":
                        print("[-] Found game")
                        if Config.ENABLE_SPEAKER:
                            state.system.speaker_engine.say("Found game")
                            state.system.speaker_engine.runAndWait()
                        state.game.state = ProgramState.SETUP
                        break
            except Exception:
                time.sleep(0.1)
                pass

    elif state.game.state == ProgramState.SETUP:
        state.game.reset()

        # wait until the game-over element disappears
        WebDriverWait(online_driver, 20).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-cy="game-over-header"]'))
        )

        # bot trying resign
        try:
            bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="resign-button-with-confirmation"]').click()
            time.sleep(0.1)
            bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="confirmation-popover-confirm-button"]').click()
            time.sleep(0.1)
        except Exception:
            pass

        # bot trying to create a new game
        try:
            bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="game-over-new-game-button"]').click()
        except Exception:
            try:
                bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="game-over-modal-new-game-button"]').click()
            except Exception:
                pass

        time.sleep(Config.UI_GAME_START_ANIMATION_DELAY)  # allow UI animation to settle

        # set up my side
        board = online_driver.find_element(By.CSS_SELECTOR, "wc-chess-board")
        board_class_name = board.get_attribute("class")
        if board_class_name == 'board':
            print("[-] Your side is white")
            state.game.my_side = Config.SIDE_WHITE
            bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="black"]').click()
        elif board_class_name == "board flipped":
            print("[-] Your side is black")
            state.game.my_side = Config.SIDE_BLACK
            bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="white"]').click()

        # bot start button click
        time.sleep(0.1)
        bot_driver.find_element(By.CSS_SELECTOR, '[data-cy="bot-selection-cta-button"]').click()
        bot_driver.execute_script("window.scrollTo(0, 0);")

        online_driver.execute_script("window.scrollTo(0, 0);") # scroll up

        time.sleep(0.3)

        find_and_apply_online_coords(state)
        find_and_apply_bot_coords(state)
        
        # set next state
        state.game.state = ProgramState.AUTO_BOT

    elif state.game.state == ProgramState.AUTO_BOT:
        if state.game.my_side == Config.SIDE_WHITE:
            move_from, move_to, state.game.bot_last_move_amount, state.game.bot_side_to_move, promoted_piece = wait_for_next_move(bot_driver, last_move_amount=state.game.bot_last_move_amount, side_to_move=state.game.bot_side_to_move, my_side=switch_side(state.game.my_side), state=state)
            from_display_posX = state.board.online_board_origin_x + (chess_to_square(move_from)[0] * state.board.online_square_size - state.board.online_square_half_size)
            from_display_posY = (state.board.online_board_origin_y + state.board.online_square_size * Config.BOARD_SIZE) - (chess_to_square(move_from)[1] * state.board.online_square_size - state.board.online_square_half_size)
            to_display_posX = state.board.online_board_origin_x + (chess_to_square(move_to)[0] * state.board.online_square_size - state.board.online_square_half_size)
            to_display_posY = (state.board.online_board_origin_y + state.board.online_square_size * Config.BOARD_SIZE) - (chess_to_square(move_to)[1] * state.board.online_square_size - state.board.online_square_half_size)
            
            simulate_thinking(get_remaining_time(online_driver, state.game.my_side),  state.game.opponent_move_time, state.game.online_move_amount)

            human_drag((from_display_posX,
                    from_display_posY),
                    (to_display_posX,
                    to_display_posY))
            try_promote_piece(promoted_piece, to_display_posX, to_display_posY)

            state.game.online_move_amount += 1

            start_opponent_time = time.time()
            move_from, move_to, state.game.online_last_move_amount, state.game.online_side_to_move, promoted_piece = wait_for_next_move(online_driver, last_move_amount=state.game.online_last_move_amount, side_to_move=state.game.online_side_to_move, my_side=state.game.my_side, state=state)
            state.game.opponent_move_time = time.time() - start_opponent_time

            if move_from is None:
                continue

            state.game.online_move_amount += 1
            
            from_display_posX = state.board.bot_board_origin_x + (chess_to_square_flipped(move_from)[0] * state.board.bot_square_size - state.board.bot_square_half_size)
            from_display_posY = (state.board.bot_board_origin_y + state.board.bot_square_size * Config.BOARD_SIZE) - (chess_to_square_flipped(move_from)[1] * state.board.bot_square_size - state.board.bot_square_half_size)
            to_display_posX = state.board.bot_board_origin_x + (chess_to_square_flipped(move_to)[0] * state.board.bot_square_size - state.board.bot_square_half_size)
            to_display_posY = (state.board.bot_board_origin_y + state.board.bot_square_size * Config.BOARD_SIZE) - (chess_to_square_flipped(move_to)[1] * state.board.bot_square_size - state.board.bot_square_half_size)

            pyautogui.moveTo(from_display_posX, from_display_posY)
            pyautogui.dragTo(to_display_posX, to_display_posY)
            try_promote_piece(promoted_piece, to_display_posX, to_display_posY)

        else: # black side
            start_opponent_time = time.time()
            move_from, move_to, state.game.online_last_move_amount, state.game.online_side_to_move, promoted_piece = wait_for_next_move(online_driver, last_move_amount=state.game.online_last_move_amount, side_to_move=state.game.online_side_to_move, my_side=state.game.my_side, state=state)
            state.game.opponent_move_time = time.time() - start_opponent_time
            
            if move_from is None:
                continue

            state.game.online_move_amount += 1

            from_display_posX = state.board.bot_board_origin_x + (chess_to_square(move_from)[0] * state.board.bot_square_size - state.board.bot_square_half_size)
            from_display_posY = (state.board.bot_board_origin_y + state.board.bot_square_size * Config.BOARD_SIZE) - (chess_to_square(move_from)[1] * state.board.bot_square_size - state.board.bot_square_half_size)
            to_display_posX = state.board.bot_board_origin_x + (chess_to_square(move_to)[0] * state.board.bot_square_size - state.board.bot_square_half_size)
            to_display_posY = (state.board.bot_board_origin_y + state.board.bot_square_size * Config.BOARD_SIZE) - (chess_to_square(move_to)[1] * state.board.bot_square_size - state.board.bot_square_half_size)
            
            pyautogui.moveTo(from_display_posX, from_display_posY)
            pyautogui.dragTo(to_display_posX, to_display_posY)
            try_promote_piece(promoted_piece, to_display_posX, to_display_posY)

            move_from, move_to, state.game.bot_last_move_amount, state.game.bot_side_to_move, promoted_piece = wait_for_next_move(bot_driver, last_move_amount=state.game.bot_last_move_amount, side_to_move=state.game.bot_side_to_move, my_side=switch_side(state.game.my_side), state=state)
            from_display_posX = state.board.online_board_origin_x + (chess_to_square_flipped(move_from)[0] * state.board.online_square_size - state.board.online_square_half_size)
            from_display_posY = (state.board.online_board_origin_y + state.board.online_square_size * Config.BOARD_SIZE) - (chess_to_square_flipped(move_from)[1] * state.board.online_square_size - state.board.online_square_half_size)
            to_display_posX = state.board.online_board_origin_x + (chess_to_square_flipped(move_to)[0] * state.board.online_square_size - state.board.online_square_half_size)
            to_display_posY = (state.board.online_board_origin_y + state.board.online_square_size * Config.BOARD_SIZE) - (chess_to_square_flipped(move_to)[1] * state.board.online_square_size - state.board.online_square_half_size)

            simulate_thinking(get_remaining_time(online_driver, state.game.my_side),  state.game.opponent_move_time, state.game.online_move_amount)

            human_drag((from_display_posX,
                from_display_posY),
                (to_display_posX,
                to_display_posY))
            try_promote_piece(promoted_piece, to_display_posX, to_display_posY)      

            state.game.online_move_amount += 1  
            
    elif state.game.state == ProgramState.GAME_OVER:
        # finding searching for a new game
        try:
            find_new_game_button = online_driver.find_element(By.CSS_SELECTOR, '[data-cy="game-over-modal-new-game-button"]')
            rand_delay(*Config.NEXT_GAME_DELAY_RANGE)
            find_new_game_button.click()

            state.game.state = ProgramState.SEARCHING_GAME
            print("[-] Searching for game")
            if Config.ENABLE_SPEAKER:
                speaker_engine.say("Searching for game")
                speaker_engine.runAndWait()
        except Exception:
            print("[E] Find new game button element not found. Retrying...")
            time.sleep(1)
            pass