from core.config import Config

def show_pre_run_info():
    print("\n⚠️ Pre-run checklist (IMPORTANT)")

    print("🔧 Chrome / System:")
    print(" - Notifications disabled")
    print(" - No system popups (e.g. default browser prompt)")

    print("\n♟️ Chess.com settings:")
    print(" - Highlight Moves = ON")
    print(" - Move Method = Drag or Click")
    print(" - Confirm resign/draw = OFF")
    print(" - Piece Notation = Text")
    print(" - Board orientation must NOT flip (always keep same perspective)")

    print("\n🤖 Bot window (RIGHT Chrome window):")
    print(" - Select bot engine (prefer stable mid-level strength)")
    print(" - Avoid maximum strength engines (e.g. 3200 Maximum)")
    print("   They may behave unnaturally and are more detectable")

    print("\n⚠️ FINAL WARNING:")
    print("Game board must be fully visible and NOT shifted or resized.")
    print("Any UI overlay or layout change may break coordinate tracking.\n")

    print("\n⚙️ FINAL SETUP STEPS:")
    print("\n1. Bring both Chrome windows to foreground (focus them)")
    print("2. RIGHT window (BOT): select the bot engine that will play for you")
    print(f"3. Press '{Config.START_BOT_KEY}' to start the bot automation")
    print(" - Bot will begin working immediately after activation key is pressed")
    print(f" - Press '{Config.QUIT_KEY}' to quit the program")