from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from pyvirtualdisplay import Display

# Only for Windows operating system
# from win32api import GetSystemMetrics
# print("Width =", GetSystemMetrics(0))
# print("Height =", GetSystemMetrics(1))

# Somehow doesn't work. Can't find the module even if it's in the pip list.
# from screeninfo import get_monitors
# for m in get_monitors():
#     print(str(m))

# import ctypes
# user32 = ctypes.windll.user32
# screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# print(screensize)
# screensize = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
# print(screensize)


# Somehow doesn't work. Can't find the module even if it's in the pip list.
# from PyQt5.QtWidgets import QApplication
# desktop = QApplication.desktop()
# screenRect = desktop.screenGeometry(1)   #2nd monitor
# print(screenRect.x(), screenRect.y())   #returns the x and y of that screen

# chrome_options = Options()
# # chrome_options.add_argument("--kiosk")
# chrome_options.addArgument("--start-maximized")
# chrome_options.add_argument('disable-infobars')
# chrome_options.add_argument("--window-size=1920,1040")
# chrome_options.add_argument("--window-position=0,0")
# driver = webdriver.Chrome(chrome_options=chrome_options)
# # driver = webdriver.Chrome()
# driver.get("https://google.com.tw")
# driver.maximize_window()

# Can't open anotehr new browser window directly right after the line above
# Have to create another webDriver.Chrome() instead
# driver.get("https://www.twitter.com")

# driver.set_window_position(150,300)

# Open anotehr page in anotehr tab.
# driver.execute_script("window.open('https://www.twitter.com', 'new window')")
# Swicth the focus back to the first tab.
# driver.switch_to_window(driver.window_handles[0])

chrome_options2 = Options()
chrome_options2.add_argument("--kiosk")
chrome_options2.add_argument('disable-infobars')
chrome_options2.add_argument("--window-size=3072,1688")
chrome_options2.add_argument("--window-position=1920,-784")
driver2 = webdriver.Chrome(chrome_options=chrome_options2)
# driver2 = webdriver.Chrome()
driver2.get("https://www.twitter.com")
# driver2.maximize_window()
