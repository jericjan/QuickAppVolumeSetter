# QuickAppVolumeSetter
Makes setting app volumes easier-ish through a GUI. I'm calling it Quavis lmao.

## Requirements:

 1. `pip install -r requirements.txt`
 2. You need [nircmd](https://www.nirsoft.net/utils/nircmd.html) installed or in the same folder as this program

## Usage:

  It's a GUI. When you first open it up, it will create a `settings.json` file for you. Open that up and edit it to your liking. `processes` is a list of process names, and `volumes` is a list of volume percentages you want for your processes. 100% is your app volume at the same volume as your system volume. Let's say your system volume is 25%. If you type in `100` in the json, the app volume will be at 25%.  
Example:  
```json
{
   "processes":[
      "BH3.exe",
      "nikke.exe"
   ],
   "volumes":[
      "5",
      "100"
   ]
}
```
