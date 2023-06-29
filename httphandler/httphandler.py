from requests import Session
from requests.adapters import HTTPAdapter
import asyncio
import logging
import os
import socket

logging.basicConfig(
    level=logging.INFO,
    filename="log.txt",
    encoding= 'utf-8',
    style = '{',
    format="{asctime},{levelname},{message}",
)

def log(text):
    return logging.info(f"{socket.gethostname()},{text}")



class HttpHandler:
    def __init__(self, address, login, password) -> None:
        self.login = login
        self.password = password
        self.address = address
        self.sn = self.create_session()
        log("Сессия создана")

    def create_session(self):
        sess = Session()
        sess.auth = (self.login, self.password)
        sess.verify = False
        sess.mount("http://", HTTPAdapter(max_retries=2))
        sess.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return sess

    # написать метод для первостепенной проверки конекта
    def get_fw_rules(self):
        return self.sn.get(
            f"http://{self.address}/api/v1/firewall/nat/port_forward", timeout=1
        )

    def set_fw_rules(self, rules, disable=None):
        response = []
        for rule in rules:
            data = {
                "id": rule["id"],
                "apply": True,
            }
            if not disable:
                data["disabled"] = False
            else:
                data["disabled"] = True
            response.append(
                self.sn.put(
                    f"http://{self.address}/api/v1/firewall/nat/port_forward",
                    json=data,
                    timeout=2,
                )
            )
        return response

# с = HttpHandler('1','2','3')