import pyautogui
import time

def display_mouse_position():
    try:
        print("Press Ctrl+C to exit.")
        while True:
            x, y = pyautogui.position()
            print(f"Mouse position: (X: {x}, Y: {y})", end='\r', flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram exited.")

if __name__ == "__main__":
    display_mouse_position()
