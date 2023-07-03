import logging
import socket
import sys
import os

from pathlib import Path



class CLogger:
    def __init__(self) -> None:
        if "Scripts" in sys.executable:
            self.logpath = Path(sys.executable).parent.parent.parent
        else:
            self.logpath = Path(sys.executable).parent

        self.logpath = Path(self.logpath, "log.txt")
        

        logging.VERBOSE = 25
        logging.addLevelName(logging.VERBOSE, "VERBOSE")
        logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(
            logging.VERBOSE, msg, *args, **kwargs
        )
        logging.verbose = lambda msg, *args, **kwargs: logging.log(
            logging.VERBOSE, msg, *args, **kwargs
        )
        
        logging.basicConfig(
            level=logging.VERBOSE,
            filename=self.logpath,
            encoding="utf-8",
            style="{",
            format="{asctime},{levelname},{message}",
        )
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def log(self, text):
        return logging.verbose(f"{socket.gethostname()},{os.getlogin()},{text}")
    
