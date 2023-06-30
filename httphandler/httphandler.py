from requests import Session
from requests.adapters import HTTPAdapter
import asyncio
import logging
import os
import socket


from c_logger import CLogger


class HttpHandler:
    def __init__(self, address, login, password) -> None:
        self.logger = CLogger()
        self.login = login
        self.password = password
        self.address = address
        self.protocol = ""
        self.sn = self.create_session()
        self.logger.log("Сессия создана")

    def create_session(self):
        sess = Session()
        sess.auth = (self.login, self.password)
        sess.verify = False
        sess.mount("http://", HTTPAdapter(max_retries=2))
        sess.mount("https://", HTTPAdapter(max_retries=2))
        sess.headers.update(
            {
                "accept": "application/json",
                "Content-Type": "application/json",
            }
        )
        return sess

    # написать метод для первостепенной проверки конекта
    def get_fw_rules(self):
        if self.protocol == "":
            self.set_protocol()
        response = self.sn.get(
            f"{self.protocol}{self.address}/api/v1/firewall/nat/port_forward",
            timeout=1,
        )
        return response

    def set_protocol(self):
        protocols = ["https://", "http://"]
        try:
            response = self.sn.get(
                f"{protocols[0]}{self.address}/api/v1/firewall/nat/port_forward",
                timeout=1,
            )
            self.protocol = protocols[0]
            return response
        except Exception as error:
            pass
        try:
            response = self.sn.get(
                f"{protocols[1]}{self.address}/api/v1/firewall/nat/port_forward",
                timeout=1,
            )
            self.protocol = protocols[1]
            return response
        except:
            pass

    def set_fw_rules(self, rules, disable=None):
        responses = []
        for rule in rules:
            data = {
                "id": rule["id"],
                "apply": True,
            }
            if not disable:
                data["disabled"] = False
            else:
                data["disabled"] = True
            try:
                response = self.sn.put(
                    f"{self.protocol}{self.address}/api/v1/firewall/nat/port_forward",
                    json=data,
                    timeout=2,
                )
            except Exception as error:
                pass
            responses.append(response)
        self.logger.log(responses)
        return responses


# с = HttpHandler('1','2','3')
