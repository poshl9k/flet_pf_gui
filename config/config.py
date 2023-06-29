import json
import os
import sys
from pathlib import Path, PurePath
import logging

class Config:
    def __init__(self) -> None:
        if "Scripts" in sys.executable:
            self.configpath = Path(sys.executable).parent.parent.parent
        else:
            self.configpath = Path(sys.executable).parent

        self.configpath = Path(self.configpath, "config.json")
        if not self.configpath.exists():
            with open(self.configpath, "w", encoding="utf-8") as wf:
                wf.write(self.create_empty_config())

        with open(self.configpath, "r", encoding="utf-8") as cf:
            config = json.load(cf)
            self.ipaddress = config["address"]
            self.login = config["login"]
            self.password = config["password"]
            self.rule_desc = config["rule-desc"].lower()

    def create_empty_config(self):
        conf_dict = {}
        conf_dict["address"] = ""
        conf_dict["login"] = ""
        conf_dict["password"] = ""
        conf_dict["rule-desc"] = ""
        return json.dumps(conf_dict)


