import subprocess
import sys
import time
import pyautogui as pag
import speech_recognition as sr
import win32com.client
import webbrowser
import pathlib
import textwrap
import google.generativeai as genai
from pynput import keyboard
import threading
from threading import Thread
import tkinter as tk

screenWidth, screenHeight = pag.size()

# testKey from my account...
mykey = "" # "---oops"
genai.configure(api_key=mykey)
model = genai.GenerativeModel('gemini-pro')
speaker = win32com.client.Dispatch("SAPI.SpVoice")

lock = threading.Lock()

def say(text):
    speaker.Speak(text)

didntUnderstandMsg = "bad audio"
def listenToCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.9
        # say("processing audio")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio_data=audio, language="en-in")
            print(f"You said: {query}")
            return query
        except Exception as e:
            say(didntUnderstandMsg)
            return "No speech detected/check internet"

# defining a site list for non-.com ending sites
siteList = {
    "vtop":".vit.ac.in",
    "vit":".ac.in",
    "wikipedia":".org",
}

def openSite(query):
    command = query.removeprefix("open ")
    # command = command + ".com"
    if command.lower() in siteList:
        extension = siteList.get(command.lower())
    else:
        extension = ".com"
    say("".join(["opening ", command.lower(), extension]))
    webbrowser.open("".join(["https://", command.lower(), extension]))

appList = {
    # Microsoft Word
    "word":"C:\Program Files\Microsoft Office\\root\Office16\WINWORD.EXE",
    "wolrd":"C:\Program Files\Microsoft Office\\root\Office16\WINWORD.EXE",

    # Microsoft PowerPoint
    "power point":"C:\Program Files\Microsoft Office\\root\Office16\POWERPNT.EXE",
    "powerpoint":"C:\Program Files\Microsoft Office\\root\Office16\POWERPNT.EXE",

    #Microsoft Excel
    "excel":"C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE",
    "exell":"C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE", # accounting for mispronounciations
    "xl":"C:\Program Files\Microsoft Office\\root\Office16\EXCEL.EXE",

    # Microsoft Access
    "msaccess": "C:\Program Files\Microsoft Office\\root\Office16\MSACCESS.EXE",
    "access": "C:\Program Files\Microsoft Office\\root\Office16\MSACCESS.EXE",
    "ms access": "C:\Program Files\Microsoft Office\\root\Office16\MSACCESS.EXE",
}

def openApp(query):
    query = query.lower()
    command = query.removeprefix("open ")
    command = command.removesuffix(" app")
    print(command, " <- identified app name")
    if(command in appList):
        command = appList.get(command)
        subprocess.Popen(command)
    else:
        try:
            command = "".join([command, ".exe"])
            subprocess.Popen(command)
        except Exception as e:
            say("Unable to find the program you are asking for...")


def typeThis(query):
    command = query.removeprefix("type ")
    if command.startswith("fullstop"):
        pag.press(".")
    if command.endswith("in upper case") or command.endswith("in uppercase"):
        command = command.removesuffix(" in upper case")
        command = command.removesuffix(" in uppercase")
        command = command.upper()
    say("".join(["typing ", command])) # test typing: Sam goes to school SAM GOES TO SCHOOL
    pag.write(command+" ")

def pressThis(query):
    query = query.replace("control", "ctrl")
    query = query.replace("delete", "del")
    query = query.replace("windows", "win")
    command = query.removeprefix("press ")
    if(command.startswith("hotkey") or command.startswith("hot key")):
        command = query.lower().removeprefix("press hot     key ");
        command = command.removeprefix("press hot key ");
        keys = command.split(" ")
        if len(keys)==3:
            pag.hotkey(keys[0], keys[1], keys[2])
        else:
            pag.hotkey(keys[0], keys[1])
    say("".join(["pressed ", command]))
    pag.press(command)

def scrollDown(clickCount):
    pag.moveTo(screenWidth / 2, screenHeight / 2)
    say("scrolling down.")
    pag.scroll(clickCount) # scroll down for specified number of clicks

# TODO: Implement emergency killswitch
stop_program=True
def on_press(key):
    global stop_program
    if key == keyboard.Key.end:
        print('End key pressed')
        stop_program = True
        # say("end")
        sys.exit()

def mouseMove(query):
    command = query.removeprefix("mouse ")
    command = command.removeprefix("Mouse ")
    command = command.split(" ")
    # print("command is: ", command, " len: ", len(command))
    direction = "left"
    if(len(command)>0):
        direction = command[0].strip()
        # say("".join(["moving ", direction]))
    points = 100
    if(len(command)>1):
        speed = command[1].strip()
        # say("".join([" in rate ", speed]))
        if(speed=="fast"):
            points = 500
        else:
            points = 10

    # say("moving mouse cursor".join([" at a speed of ", str(points)]))
    if(direction=="left"):
        x, y = pag.position()
        # say("".join(["mouse is currently at", str(x), " and ", str(y)]))
        pag.moveTo(x-points, y)
    if (direction == "right"):
        x, y = pag.position()
        # say("".join(["mouse is currently at", str(x), " and ", str(y)]))
        pag.moveTo(x + points, y)
    if (direction == "up" or direction=="above"):
        x, y = pag.position()
        # say("".join(["mouse is currently at", str(x), " and ", str(y)]))
        pag.moveTo(x, y - points)
    if (direction == "down" or direction=="below"):
        x, y = pag.position()
        # say("".join(["mouse is currently at", str(x), " and ", str(y)]))
        pag.moveTo(x, y + points)

# if __name__=='__main__':
inConvoMode = False

#
# if __name__ == '__main__':
#     # Create threads
#     thread1 = threading.Thread(target=create_window)
#     thread2 = threading.Thread(target=main)
#
#     # Start threads
#     thread1.start()
#     thread2.start()
#
#     # Wait for threads to finish (optional)
#     thread1.join()
#     thread2.join()

# import tkinter as tk
# import sys

def display_text(text):
    label.config(text=text)

# def indicate():
#     root = tk.Tk()
#     root.title("AutoOrange - Voice Assistant")
#     root.geometry("150x150+30+30")  # Set width, height, x-pos, y-pos
#     root.wm_attributes('-topmost', True)  # Stay on top
#
#     # Override withdraw/deiconify approach for a more direct solution
#     root.overrideredirect(True)  # Remove window decorations (title bar, etc.)
#
#     label = tk.Label(root, text="")
#     label.pack(padx=10, pady=50)
#
#     display_text(sys.argv[1])
#
#     x = y = 0
#
#
#     def start_move(event):
#         global x, y
#         x = event.x
#         y = event.y
#
#
#     def move_window(event):
#         dx = event.x - x
#         dy = event.y - y
#         root.geometry(f"150x150+{root.winfo_rootx() + dx}+{root.winfo_rooty() + dy}")
#
#
#     # Bind events for dragging the window
#     root.bind("<Button-1>", start_move)
#     root.bind("<B1-Motion>", move_window)
#
#     root.mainloop()  # Start the main event loop for Tkinter

from multiprocessing import Process

# if __name__ == "__main__":
#   indicateProcess = Process(target=indicate)
#   process_two = Process(target=function_two)
#
#   process_one.start()  # Launch function_one in a separate process
#   process_two.start()  # Launch function_two in a separate process

  # Optional: Wait for processes to finish (if needed)
  # process_one.join()
  # process_two.join()


def main():
    global inConvoMode
    print('--- PROGRAM START ---')
    # lock.acquire(False)
    # indicatorInstance = subprocess.Popen(["python", "indicator.py", "AutoOrange\nRUNNING"])
    # subprocess.Popen(["python", "indicator.py", "AutoOrange\nRUNNING"])
    say("Launched successfully!")
    # lock.release()
    # indicatorWindow = subprocess.Popen(["python", "indicator.py", "Launching..."])
    while(1):
        print("Listening...")
        say(". speak ")
        # indicatorWindow.kill()
        # indicatorWindow = subprocess.Popen(["python", "indicator.py", "Listening..."])
        # pag.hotkey("alt", "tab")
        command = listenToCommand()
        # indicatorWindow.kill()
        # indicatorWindow = subprocess.Popen(["python", "indicator.py", "Processing your voice input..."])
        # pag.hotkey("alt", "tab")
        # command = input()
        queries = []
        if "then orange" or "then Orange" in command.lower():
            print("multi-command identified")
            comms = command.split("then orange ")
            comms = command.split("then Orange ")
            for i in comms:
                queries.append(i.rstrip(" ").lstrip(" "))
            # queries = command.partition("then autobot")
            # queries = command.partition("then Autobot")
        else:
            queries = [command]
        print(queries)
        flag = 0
        for query in queries:
            # if query!=didntUnderstandMsg:
            if query.lower().startswith("open") and not query.lower().endswith(" app"):
                openSite(query)
            elif query.lower().startswith("open") and query.lower().endswith(" app"):
                openApp(query)
            elif query.lower().startswith("type"):
                typeThis(query)
            elif query.lower().startswith("press"):
                pressThis(query)
            elif query.lower().startswith("scroll down"):
                scrollDown(-50)
            elif query.lower().startswith("scroll up"):
                scrollDown(50)
            elif query.lower().startswith("mouse"):
                mouseMove(query)
            elif query.lower().startswith("click"):
                pag.click()
            elif query.lower().startswith("right click"):
                pag.rightClick()
            elif query.lower().startswith("right click"):
                pag.doubleClick();
            elif query.lower().startswith("hold"):
                pag.mouseDown()
            elif query.lower().startswith("unhold"):
                pag.mouseUp()
            elif query.lower().startswith("bye bye orange") or query.lower().startswith("bye bye Orange") or query.lower().startswith("bye-bye orange") or query.lower().startswith("bye-bye Orange"):
                print("--- PROGRAM END ---")
                indicatorInstance.kill()
                indicatorInstance = subprocess.Popen(["python", "indicator.py", "Shutting down\nAutoOrange"])
                say("shutting down! See you again!")
                indicatorInstance.kill()
                flag = 1  # close program
                sys.exit()
                break
            elif query.lower().startswith("enter conversation mode") or query.lower().startswith("inter conversation mode"):
                print("---CONVERSATION MODE START---")
                # search on web/ integrate with chatGPT
                say("Conversation mode. Talk to an AI!")
                indicator = subprocess.Popen(["py", "indicator.py", "Conversation"])
                while(True):
                    inConvoMode = True
                    # indicatorWindow.kill()
                    # indicatorWindow = subprocess.Popen(["python", "indicator.py", "Conversation mode..."])
                    # pag.hotkey("alt", "tab")
                    print("Listening...")
                    say(". speak")
                    command = listenToCommand()
                    # command = input()
                    # print("convo loop start")
                    if command.startswith("exit conversation mode"):
                        # inConvoMode = False
                        indicator.kill()
                        break
                    else:
                        response = model.generate_content(command)
                        print(response.text)
                        # indicatorWindow.kill()
                        # indicatorWindow = subprocess.Popen(["python", "indicator.py", response.text])
                        # pag.hotkey("alt", "tab")
                        say(response.text)
                    # with keyboard.Listener(on_press=on_press) as listener:
                    #     # try:
                    #     audio_thread = threading.Thread(target=say("this program sure is executing in all its glory but I wonder if it can be stopped at any time"))
                    #     audio_thread.start()
                    #     while not stop_program and audio_thread.is_alive():
                    #         pass
                    #     if stop_program:
                    #         print('Program terminated by user')
                    #         audio_thread.
                    #         sys.exit()
                    #     except SystemExit:
                    #         print("terminated by user successfully")
                print("---CONVERSATION MODE END---")
                say("Ending conversation mode")

            # time.sleep(3)
            # say(query)
        if flag==1:
            break
        # time.sleep(0.5) # some delay for the user to prepare next command
main()