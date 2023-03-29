import logging
import os
from datetime import datetime
import sys


#The Name of Logging File
LOG_FILE_NAME = f"{datetime.now().strftime('%d%m%y__%H%M%S')}.log"

#The Folfer for logs
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#Create Folder is not exsits
os.makedirs(LOG_FILE_DIR,exist_ok=True)

#Inputting log file name into log directory
LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

#configuring logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

