import time
import keyboard
from PIL import ImageGrab

def screenshot():
    curr_time = time.strftime("_%Y%m%d_%H%M%S")
    img = ImageGrab.grab()
    img.save("image{}.png".format(curr_time))
    
keyboard.add_hotkey("a", screenshot) #when F9 pressed, save screenshot
# keyboard.add_hotkey("ctrl+shift+s")

keyboard.wait("esc") #run till esc pressed