import tkinter as tk
import sys

def display_text(text):
    label.config(text=text)


root = tk.Tk()
root.title("AutoOrange - Voice Assistant")
root.geometry("150x150+30+30")  # Set width, height, x-pos, y-pos
root.wm_attributes('-topmost', True)  # Stay on top

# Override withdraw/deiconify approach for a more direct solution
root.overrideredirect(True)  # Remove window decorations (title bar, etc.)

label = tk.Label(root, text="")
label.pack(padx=10, pady=50)

display_text(sys.argv[1])

x = y = 0


def start_move(event):
    global x, y
    x = event.x
    y = event.y


def move_window(event):
    dx = event.x - x
    dy = event.y - y
    root.geometry(f"150x150+{root.winfo_rootx() + dx}+{root.winfo_rooty() + dy}")


# Bind events for dragging the window
root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", move_window)

root.mainloop()  # Start the main event loop for Tkinter
