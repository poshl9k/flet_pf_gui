from requests import Session


class HttpHandler:
    
    
    def __init__(self,address,login='admin',password='routeradmin789') -> None:
        self.sn = self.create_session()
        self.login = login
        self.password = password
        self.address = address


    def create_session(self):
        sess = Session()
        sess.auth = (self.login,self.password)
        return sess
    
    
    def get_fw_rules(self):
        return self.sn.get('https://pfsense.example.com/api/v1/firewall/rule')