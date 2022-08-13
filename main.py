"""
The Main File
    compile this
"""

from tkinter import Tk, Button
from tkinter.messagebox import showinfo
from subprocess import Popen, PIPE
import os
import json
from functools import partial
import sys


def bruh_moment(msg):
    """Sends a pop-up message and exits. Usually a user error"""
    showinfo(title="Bruh.", message=msg)
    sys.exit()


if os.path.exists("settings.json"):
    with open("settings.json", encoding="utf-8") as f:
        try:
            json_dict = json.load(f)
        except:
            bruh_moment(
                "This file is invalid. You somehow broke it. Let me guess. You forgot a comma."
            )
    try:
        process_name = json_dict["process"]
        if not isinstance(process_name, str):
            raise Exception
        volumes = json_dict["volumes"]
        if not isinstance(volumes, list):
            raise Exception
    except Exception as e:
        bruh_moment(
            "Something is missing in the file. It should have a process and a list of volumes."
        )

    if json_dict["process"] == "PROCESS_NAME_HERE":
        bruh_moment(
            'I told you to edit the "settings.json" file.\n'
            "Change the process name to something else (with .exe)."
        )
    else:
        pass
else:
    json_dict = {}
    json_dict["process"] = "PROCESS_NAME_HERE"
    json_dict["volumes"] = ["0", "100"]
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(json_dict, f, indent=4)
    showinfo(
        title="YO!",
        message='I have create a "settings.json" file. Open that up and edit in your stuff.',
    )
    sys.exit()


def find_proc(proc_name):
    "Finds the PID given the process name"
    coms = ["tasklist", "|", "findstr", proc_name]
    with Popen(coms, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True) as proc:
        stdout, stderr = proc.communicate()
    items = stdout.decode("utf-8").split(" ")
    items = [x for x in items if x]
    try:
        proc_id = items[1]
    except:
        bruh_moment(f"Damn. I can't find {proc_name}")
    return proc_id


def set_vol(p_id, val):
    "Sets the volume of a process w/ nircmd given the PID"
    coms = ["nircmd", "setappvolume", f"/{p_id}", val]
    with Popen(coms, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
    if stderr:
        bruh_moment("You don't have nircmd installed or in the current folder.")
    print(f"Volume set to {val}")


def change_vol(percent):
    "Calls two functions which find the process and sets its volume"
    proc_id = find_proc(process_name)
    print(f"Setting {proc_id} to {percent}...")
    set_vol(proc_id, percent)


window = Tk()


def make_buttons():
    "Creates the buttons that will be shown on the GUI"
    for volume in volumes:
        human_volume = f"{volume}%"
        fixed_volume = str(int(volume) / 100)
        button = Button(
            window,
            text=human_volume,
            width=10,
            command=partial(change_vol, fixed_volume),
        )
        button.pack()


make_buttons()


window.title("Volume Setter")
window.attributes("-topmost", True)
window.update()
window.geometry("300x50")
window.mainloop()
