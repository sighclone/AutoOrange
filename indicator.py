import tkinter as tk
import sys
import pyautogui

def display_text():
  """Gets the system argument or sets default text and displays it on the window."""
  text = "Hello World"
  if len(sys.argv) > 1:
    text = sys.argv[1]
  label.config(text=text)

root = tk.Tk()
root.title("AutoOrange - Voice Assistant")
root.geometry("150x150+0+0")  # Set width, height, x-pos, y-pos
root.wm_attributes('-topmost', True)  # Stay on top

# Override withdraw/deiconify approach for a more direct solution
root.overrideredirect(True)  # Remove window decorations (title bar, etc.)

label = tk.Label(root, text="")
label.pack(padx=10, pady=50)

display_text()

root.mainloop()
