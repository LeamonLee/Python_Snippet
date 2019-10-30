from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import six
import os, sys, time

def checkNodeisUp():
    
    proc1 = subprocess.Popen(['ps', 'ax'], stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['grep', 'node'], stdin=proc1.stdout,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc1.stdout.close()                # Allow proc1 to receive a SIGPIPE if proc2 exits.
    # out, err = proc2.communicate()
    out = proc2.communicate()[0]
    out = out.decode("utf-8")
    isFound = False
    for result in out.split('\n'):
        if 'server.js' in result:
            isFound = True
            print('result: ', result)

    return isFound

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

        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) 

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


dictStartPos = {"nStartPosX": 0,
                "nStartPosY": 0,
                "nStartSecondPosX": 0,
                "nStartSecondPosY": 0,
                "nStartThirdPosX": 0,
                "nStartThirdPosY": 0,
                "nStartFourthPosX": 0,
                "nStartFourthPosY": 0,
                "nStartFifthPosX": 0,
                "nStartFifthPosY": 0
}

if __name__ == "__main__":
    
    nRetry = 0
    while nRetry < 30:
        print("Search node server.js...")
        result = checkNodeisUp()
        if result:
            break
        time.sleep(1)
        nRetry += 1
        if nRetry >= 30:
            print("TimeOut! Node server.js is not found!")
            sys.exit(0)
        

    lstWindowSize = checkResolution()

    if len(lstWindowSize) > 0:
        # lstUrl = ["https://google.com.tw", "https://www.twitter.com", "https://www.facebook.com.tw", "https://www.bitrix24.com/"]
        strFilePrefix = "file:///"
        strPath = os.path.dirname(os.path.abspath(__file__)) + '/'
        strUrl1 = "localhost:3000"
        strUrl2 = strFilePrefix + strPath + "demo2.html"
        strUrl3 = strFilePrefix + strPath + "demo3.html"
        strUrl4 = strFilePrefix + strPath + "demo4.html"
        strUrl5 = strFilePrefix + strPath + "demo5.html"
        # print(strUrl1)
        # print(strUrl2)

        lstUrl = [strUrl1, strUrl2, strUrl3, strUrl4, strUrl5]
        for idx, pos in enumerate(lstWindowSize):
            if 'x' in pos:
                lstPos = pos.split('x')
                if idx == 0:
                    
                    print(dictStartPos["nStartPosX"], dictStartPos["nStartPosY"])
                    print("lstWindowSize: ", lstWindowSize)
                    nSizeX = int(lstPos[0])
                    nSizeY = int(lstPos[1])
                    
                    lstPos = [dictStartPos["nStartPosX"], dictStartPos["nStartPosY"]]
                    
                    dictStartPos["nStartSecondPosX"] = dictStartPos["nStartPosX"] + nSizeX
                    dictStartPos["nStartSecondPosY"] = dictStartPos["nStartPosY"]
                    dictStartPos["nStartThirdPosX"] = dictStartPos["nStartPosX"]
                    dictStartPos["nStartThirdPosY"] = dictStartPos["nStartPosY"] + nSizeY
                    dictStartPos["nStartFourthPosX"] = dictStartPos["nStartPosX"] + nSizeX
                    dictStartPos["nStartFourthPosY"] = dictStartPos["nStartPosY"] + nSizeY
                    
                elif idx == 1:
                    lstPos = [dictStartPos["nStartSecondPosX"], dictStartPos["nStartSecondPosY"]]
                    
                    dictStartPos["nStartFifthPosX"] = dictStartPos["nStartSecondPosX"] + int(lstPos[0])
                    dictStartPos["nStartFifthPosY"] = dictStartPos["nStartSecondPosY"]
                elif idx == 2:
                    
                    lstPos = [dictStartPos["nStartThirdPosX"], dictStartPos["nStartThirdPosY"]]
                elif idx == 3:
                    
                    lstPos = [dictStartPos["nStartFourthPosX"], dictStartPos["nStartFourthPosY"]]
                elif idx == 4:
                    
                    lstPos = [dictStartPos["nStartFifthPosX"], dictStartPos["nStartFifthPosY"]]
                lstsize = [-1,-1]                                           # -1 means to use the maximum size
                print(idx, " ",lstPos)
                startUpBrowser(lstUrl[idx], lstsize, lstPos, True)

    
    print("Done!")