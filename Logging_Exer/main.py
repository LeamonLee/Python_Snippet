import os, logging, datetime

logger = logging.getLogger(__name__)

rootPath = os.path.dirname(os.path.abspath(__file__))
dirpath = os.path.join(rootPath, "LOG")
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

strToday = datetime.date.today()
strToday = strToday.strftime("%Y-%m-%d")

logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s - %(lineno)s] %(message)s')
file_handler = logging.FileHandler(f'{dirpath}/{strToday}.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

if __name__ == "__main__":

    logger.info("Task Scheduler works!")

