import os
import inspect
import logging
from datetime import datetime

def customLogger(logLevel=logging.INFO):
    # Create the directory for logs if it doesn't exist
    log_dir = "AutoLogs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Gets the name of the class / method from where this method is called
    stack = inspect.stack()
    loggerName = stack[1][3]
    moduleName = stack[1][1]
    logger = logging.getLogger(loggerName)
    # By default, log all messages
    logger.setLevel(logLevel)

    # Check if the logger already has handlers
    if not logger.handlers:
        current_time = datetime.strftime(datetime.now(), '%d_%m_%Y_%I_%M_%S%p')
        log_file = os.path.join(log_dir, f"Demo_{current_time}.log")
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setLevel(logLevel)

        formatter = logging.Formatter('%(asctime)s - %(module)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d_%m_%Y %I:%M:%S %p')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    return logger