import pyautogui
import time

time.sleep(3)
for i in range(10):
    #run rhino-python script
    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'alt', 'r')
    time.sleep(1)

    # swap applications
    pyautogui.hotkey('command', 'tab')





#AABBRrrRRRr