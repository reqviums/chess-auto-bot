import pyautogui
import random
import time
from core.config import Config

def rand_delay(a, b):
    time.sleep(random.uniform(a, b))

def rand_offset(x, y, r=Config.RAND_OFFSET_PIXELS):
    return x + random.randint(-r, r), y + random.randint(-r, r)

def human_move_to(x, y):
    x, y = rand_offset(x, y)

    pyautogui.moveTo(
        x, y,
        duration=random.uniform(*Config.MOUSE_BASE_MOVE_DURATION_RANGE),
        tween=pyautogui.easeInOutQuad
    )

def human_click(x, y):
    x, y = rand_offset(x, y)

    human_move_to(x, y)
    rand_delay(0.05, 0.15)

    pyautogui.mouseDown()
    rand_delay(*Config.MOUSE_CLICK_DOWN_UP_DELAY_RANGE)
    pyautogui.mouseUp()


def human_drag(start, end):
    sx, sy = rand_offset(*start)
    ex, ey = rand_offset(*end)

    if random.random() < Config.HUMAN_DRAG_MIDPOINT_CHANCE:
        mx = (sx + ex) // 2 + random.randint(-Config.HUMAN_DRAG_MIDPOINT_OFFSET, Config.HUMAN_DRAG_MIDPOINT_OFFSET)
        my = (sy + ey) // 2 + random.randint(-Config.HUMAN_DRAG_MIDPOINT_OFFSET, Config.HUMAN_DRAG_MIDPOINT_OFFSET)

        pyautogui.moveTo(sx, sy, duration=random.uniform(*Config.MOUSE_BASE_MOVE_DURATION_RANGE))
        pyautogui.mouseDown()

        pyautogui.moveTo(mx, my, duration=random.uniform(*Config.MOUSE_MIDPOINT_DURATION_RANGE))
        pyautogui.moveTo(ex, ey, duration=random.uniform(*Config.MOUSE_BASE_MOVE_DURATION_RANGE))

        pyautogui.mouseUp()
    else:
        pyautogui.moveTo(sx, sy, duration=random.uniform(*Config.MOUSE_BASE_MOVE_DURATION_RANGE))
        pyautogui.mouseDown()

        pyautogui.moveTo(
            ex, ey,
            duration=random.uniform(*Config.MOUSE_DRAG_DURATION_RANGE),
            tween=pyautogui.easeInOutQuad
        )

        pyautogui.mouseUp()
