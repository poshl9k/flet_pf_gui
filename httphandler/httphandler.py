from requests import Session
import asyncio

class HttpHandler:
    
    
    def __init__(self,address='192.168.0.150',login='admin',password='routeradmin789') -> None:
        self.login = login
        self.password = password
        self.address = address
        self.sn = self.create_session()


    def create_session(self):
        sess = Session()
        sess.auth = (self.login,self.password)
        sess.verify = False
        return sess
    
    
    def get_fw_rules(self):
        return self.sn.get(f'http://{self.address}/api/v1/firewall/rule')
    
import json 
s = HttpHandler(address='192.168.10.8',login='admin',password='123qwe123***')
response = json.loads(s.get_fw_rules().text)['data']
pass