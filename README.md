# ♟️ Chess.com Auto Bot

## 📌 Overview

This project is an automated chess bot that plays games on your behalf against real players.

The bot works by:

* Parsing moves directly from the website (e.g. Chess.com)
* Reconstructing the board state internally
* Simulating mouse movement and clicks to make moves
* Adding realistic delays to mimic human thinking

The thinking time is dynamic — as the game progresses and the timer decreases, the bot starts playing faster, similar to how a real player behaves under time pressure.

After a game finishes, the bot will automatically start a new game after a short delay.

## 🎥 Video Showcase

Watch the bot in action:
[![Showcase](https://i3.ytimg.com/vi/zb3kWhO9X4Y/hqdefault.jpg)](https://www.youtube.com/watch?v=zb3kWhO9X4Y)

---

## ⚙️ How It Works

1. The bot reads moves from the website using parsing
2. It calculates the next move using a selected engine
3. It simulates:

   * Mouse movement
   * Piece dragging or clicking
4. It introduces delays to imitate human thinking

⚠️ The bot does NOT use an API — everything is done through browser interaction and input simulation.

---

## 🧰 Requirements

* Python 3.x
* Google Chrome browser
* Windows OS

✅ Tested environment:

* Windows 11 (build 26200.8246)
* Display scale: **100%**
* Last tested: **04/29/2026**

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Configure paths

Open `config.py` and update the following if needed:

```python
CHROME_PATH = "path/to/your/chrome"
ONLINE_PROFILE_DIR = "path/to/your/profile"
BOT_PROFILE_DIR = "path/to/bot/profile"
```

---

### 3. Run the script

After launching:

1. Bring both Chrome windows to foreground (focus them)
2. RIGHT window (BOT): select the bot engine that will play for you
3. Press **`w`** to start the bot automation

The bot will begin working immediately after the activation key is pressed.

---

## ⚠️ Important Usage Rules

* Do NOT use your mouse or keyboard while the bot is running
* Any manual input may break the automation
* Keep both browser windows visible and unchanged

---

## ⚙️ Configuration & Setup

### ⚠️ Pre-run checklist (IMPORTANT)

#### 🔧 Chrome / System:

* Notifications **disabled**
* No system popups (e.g. default browser prompts)

#### ♟️ Chess.com settings:

* Highlight Moves = **ON**
* Move Method = **Drag or Click**
* Confirm resign/draw = **OFF**
* Piece Notation = **Text**
* Board orientation must **NOT flip** (always keep same perspective)

---

### 🤖 Bot Window (RIGHT Chrome window)

* Select a bot engine (recommended: stable mid-level strength)
* Avoid maximum strength engines (e.g. 3200+)

These may:

* behave unnaturally
* increase detection risk

---

### 📐 Board Requirements

* The game board must be fully visible
* Do NOT resize or move it
* No overlays or UI changes

Any layout shift may break coordinate tracking.

---

## ❗ Disclaimer

This project is for educational purposes only.

Using automation tools in online games may violate the platform’s terms of service and can result in account penalties.

---

## 🛠 Tech Stack

* Python
* Browser automation (input simulation)
* Parsing logic for move detection

---

## 📬 Notes

This bot relies heavily on:

* Screen coordinates
* UI consistency
* Timing simulation

If something breaks — it’s usually due to layout or environment changes.
