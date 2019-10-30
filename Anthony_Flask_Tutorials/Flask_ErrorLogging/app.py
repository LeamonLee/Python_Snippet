from flask import Flask
import logging                  # When importing logging, it won't import logging.handlers for you automatically.
import logging.handlers
# from logging.handlers import RotatingFileHandler
import os 
import sys
import datetime
from enum import Enum


app = Flask(__name__)
m_filePath = os.path.dirname(os.path.realpath(__file__))
# m_filePath = os.getcwd()
# print(m_filePath)
m_LogDirectoryPath = m_filePath + "/LOG"

LoggerType = Enum("LoggerType", "DEFAULT ROTATING TIMED")



def setup_custom_logger(_loggerName, _filePath, _mode='w', _logType=LoggerType.DEFAULT):
    if not os.path.exists(m_LogDirectoryPath):
        os.makedirs(m_LogDirectoryPath)

    formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)-8s %(message)s ' + 
                                    '(%(filename)s:%(funcName)s():%(lineno)s)', datefmt='%Y-%m-%d %H:%M:%S')
    
    if _logType == LoggerType.ROTATING:
        _fileSize = 100 * 1024 * 1024       # 100MB = 100 * 1024 KB = 100 * 1024 * 1024 Bytes
        file_handler = logging.handlers.RotatingFileHandler(_filePath, maxBytes=2000, backupCount=7)
    elif _logType == LoggerType.TIMED:
        '''
        when='midnight' is a special case, in that the interval parameter is not used, 
        and the log is rolled over on a daily basis at midnight, 
        regardless of the time when the script is launched.
        'S': Seconds, 'M':Minutes, 'H':Hours, 'D': Days, 'W': WeekDay(0=Monday), 'midnight':Roll over at midnight
        '''
        file_handler = logging.handlers.TimedRotatingFileHandler(_filePath, when='midnight', interval=1, backupCount=7)
        file_handler.suffix = "%Y%m%d-%H%M.log"
        
    else:
        file_handler = logging.FileHandler(_filePath, mode=_mode, encoding='UTF-8')
    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    screen_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger(_loggerName)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(screen_handler)

    if not app.debug:
        # file_handler2 = logging.FileHandler("errorlog.txt")
        # file_handler2.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

    return logger


@app.errorhandler(500)
def internal_error(exception):
    m_appLogger.info("Soemthing wrong happened!")
    
    app.logger.error(exception)
    # return render_template('error_500.html'), 500
    return "oops, something wrong happened.", 500


@app.route("/")
def index():
    m_appLogger.info("Hello index()!")
    return 1 / 0             # Just a contrived example
    # return "Hello Logger!"


if __name__ == "__main__":
    # tempFileName = datetime.datetime.now().strftime("%Y%m%d") + ".log"
    tempFileName = "Log_"
    m_logFileName = m_LogDirectoryPath + '/' + tempFileName
    m_appLogger = setup_custom_logger('myapp', m_logFileName, 'a', LoggerType.TIMED)      # 'a': append, 'w':overwrite

    app.run(debug=False, host="0.0.0.0", port=5000)