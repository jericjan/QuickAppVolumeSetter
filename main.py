"""
The Main File
    compile this
"""

from tkinter import Tk, Button, Frame, Listbox, Variable
from tkinter.messagebox import showinfo
from subprocess import Popen, PIPE
import os
import json
from functools import partial
import sys
import threading
import time
from pathlib import Path

def bruh_moment(msg, do_exit=True):
    """Sends a pop-up message and exits. Usually a user error"""
    showinfo(title="Bruh.", message=msg)
    if do_exit:
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
        processes = json_dict["processes"]
        if not isinstance(processes, list):
            raise Exception
        volumes = json_dict["volumes"]
        if not isinstance(volumes, list):
            raise Exception
    except Exception as e:
        bruh_moment(
            "Something is missing in the file. It should have a process and a list of volumes."
        )

    if json_dict["processes"] == ['app1.exe', 'app2.exe']:
        bruh_moment(
            'I told you to edit the "settings.json" file.\n'
            "Change the process name to something else (with .exe)."
        )
    else:
        pass
else:
    json_dict = {}
    json_dict["processes"] = ['app1.exe', 'app2.exe']
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
        bruh_moment(f"Damn. I can't find {proc_name}", do_exit=False)
    return proc_id


def set_vol(p_id, val):
    "Sets the volume of a process w/ nircmd given the PID"
    nircmd_path = Path(__file__).resolve().with_name("nircmd.exe")
    coms = [nircmd_path, "setappvolume", f"/{p_id}", val]
    with Popen(coms, stdin=PIPE, stdout=PIPE, stderr=PIPE) as proc:
        stdout, stderr = proc.communicate()
    if stderr:
        bruh_moment("You don't have nircmd installed or in the current folder.")
    print(f"Volume set to {val}")

def get_selected_process():
    process = [l_box.get(x) for x in l_box.curselection()]
    process= process[0] if process else None
    return process

def find_proc_and_set_vol(process_name, percent):
    proc_id = find_proc(process_name)
    print(f"Setting {proc_id} to {percent}...")
    set_vol(proc_id, percent)

def change_vol(percent):
    "Calls two functions which find the process and sets its volume"
    process_name = get_selected_process()
    if process_name:
        thread = threading.Thread(target=find_proc_and_set_vol, args=[process_name, percent])
        thread.start()        
    else:
        bruh_moment("You did not select a process!", do_exit=False)

window = Tk()


def make_buttons():
    "Creates the buttons that will be shown on the GUI"
    games_frame = Frame()
    games_frame.pack()
    global l_box 
    l_box = Listbox(
        games_frame,
        height=3,
        listvariable=Variable(value=processes),
    )
    l_box.pack()        

    vols_frame = Frame()
    vols_frame.pack()
    for volume in volumes:
        human_volume = f"{volume}%"
        fixed_volume = str(int(volume) / 100)
        button = Button(
            vols_frame,
            text=human_volume,
            width=10,
            command=partial(change_vol, fixed_volume),
        )
        button.pack()


make_buttons()

def test():
    global l_box 
    while True: 
        print([l_box.get(x) for x in l_box.curselection()])
        time.sleep(1)

# thread = threading.Thread(target=test)
# thread.start()
window.title("Volume Setter")
window.attributes("-topmost", True)
window.update()
window.geometry(f"300x{window.winfo_height()+10}")
window.mainloop()
