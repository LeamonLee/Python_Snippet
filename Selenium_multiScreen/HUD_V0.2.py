from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import six
import os

def checkResolution():

    resSize = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]

    if isinstance(resSize, six.string_types):
        resSize = resSize.split('\n')
    elif isinstance(resSize, bytes):
        resSize = resSize.decode("utf-8").split('\n')
    
    print(resSize)
    return resSize

def startUpBrowser(strUrl, lstWindowSize, lstPosition, bKiosk=False):
    chrome_options = Options()
    bMaximumSize = False
    try:
        if bKiosk:
            chrome_options.add_argument("--kiosk")
            chrome_options.add_argument('disable-infobars')
        else:
            if isinstance(lstWindowSize, list) and lstWindowSize[0] >= 0:
                chrome_options.add_argument("--window-size={0},{1}".format(lstWindowSize[0], lstWindowSize[1]))
            else:
                bMaximumSize = True
                print("--start-maximized")
                chrome_options.add_argument("--start-maximized")
        
        if isinstance(lstPosition, list) and len(lstPosition) == 2:
            chrome_options.add_argument("--window-position={0},{1}".format(lstPosition[0], lstPosition[1]))
        else:
            print("lstPosition is incorrect!!!")
            return
        
        chrome_options.add_argument("--no-sandbox")
        # To keep the browers open after the python program finishes.
        chrome_options.add_experimental_option("detach", True)

        strPath = os.path.dirname(os.path.abspath(__file__)) + '/' +"chromedriver"
        print("strPath: ", strPath)
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=strPath)
        if isinstance(strUrl, six.string_types):
            driver.get(strUrl)

            if not bKiosk and bMaximumSize:
                driver.maximize_window()
            print("{0} is running...".format(strUrl))
        else:
            print("strUrl is incorrect!!!")
    except Exception as e:
        print("Something wrong happened: ", e)
        driver.close()


if __name__ == "__main__":
    
    lstWindowSize = checkResolution()
    nStartPosX = 0
    nStartPosY = 0
    nStartFourthPosX = 0
    nStartFourthPosY = 0

    if len(lstWindowSize) > 0:
        # lstUrl = ["https://google.com.tw", "https://www.twitter.com", "https://www.facebook.com.tw", "https://www.bitrix24.com/"]
        strFilePrefix = "file:///"
        strPath = os.path.dirname(os.path.abspath(__file__)) + '/'
        strUrl1 = strFilePrefix + strPath + "demo1.html"
        strUrl2 = strFilePrefix + strPath + "demo2.html"
        print(strUrl1)
        print(strUrl2)

        lstUrl = [strUrl1, strUrl2, "https://www.facebook.com.tw", "https://www.bitrix24.com/"]
        for idx, pos in enumerate(lstWindowSize):
            if 'x' in pos:
                lstPos = pos.split('x')
                if idx == 0:
                    print(nStartPosX, nStartPosY)
                    lstPos = [nStartPosX, nStartPosY]
                elif idx == 1:
                    print(nStartPosX + int(lstPos[0]), nStartPosY)
                    nStartFourthPosX = nStartPosX + int(lstPos[0])
                    nStartFourthPosY = nStartPosY + int(lstPos[1])
                    lstPos = [nStartPosX + int(lstPos[0]), nStartPosY]
                elif idx == 2:
                    print(nStartPosX, nStartPosY + int(lstPos[1]))
                    lstPos = [nStartPosX, nStartPosY + int(lstPos[1])]
                elif idx == 3:
                    print(nStartFourthPosX, nStartFourthPosY)
                    lstPos = [nStartFourthPosX, nStartFourthPosY]
                lstsize = [-1,-1]                                           # -1 means to use the maximum size
                
                startUpBrowser(lstUrl[idx], lstsize, lstPos, True)

    
    print("Done!")