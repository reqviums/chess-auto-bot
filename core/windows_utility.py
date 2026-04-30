import win32api
import tkinter as tk

def get_default_title_bar_height() -> int:
    root = tk.Tk()
    root.update_idletasks()
    root.update()
    title_bar = root.winfo_rooty() - root.winfo_y()

    root.destroy()

    return title_bar

def get_primary_monitor_work_area():
    work_area = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))["Work"]
    left, top, right, bottom = work_area

    return left, top, right, bottom

def get_dual_window_layout(left, top, right, bottom):
        width = right - left
        height = bottom - top

        return {
            "left_window": (left, top, width // 2, height),
            "right_window": (left + width // 2, top, width // 2, height),
        }
def apply_rect_chrome_window(driver, x, y, w, h):
    driver.set_window_position(x, y)
    driver.set_window_size(w, h)

def apply_dual_chrome_layout(online_driver, bot_driver):
    left, top, right, bottom = get_primary_monitor_work_area()
    layout = get_dual_window_layout(left, top, right, bottom)

    apply_rect_chrome_window(online_driver, *layout["left_window"])
    apply_rect_chrome_window(bot_driver, *layout["right_window"])