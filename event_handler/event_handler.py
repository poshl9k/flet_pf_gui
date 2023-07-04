import time
import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
    icons,
    Divider,
    RoundedRectangleBorder,
    ButtonStyle,
    MaterialState,
    IconButton,
    FilledButton,
    TextTheme,
    TextAlign,
    FloatingActionButton,
    Alignment,
    Scale,
    Icon,
    margin,
    SnackBar,
)
from httphandler import HttpHandler
import json
from .alerts import Alerts
import asyncio
from threading import Thread
from config import Config


from c_logger import CLogger


class EventHandler:
    """
    gui:PfsenseApiApp
    """

    def __init__(self, gui) -> None:
        self.gui = gui
        self.cf = Config()
        self.logger = CLogger()
        self.http_session = None
        self.nat_rules = list()
        self.nat_rule_desc = self.cf.rule_desc
        self.router_status = False
        self.logger.log("Цикл событий инициализирован")

    def handle_event(self, event):
        data = event.control.data
        if data == "Connect_to_router":
            self.connect_to_router()
            self.logger.log("Подключение к роутеру")
        if data == "enable_cameras":
            self.logger.log(f"Нажата кнопка Включить доступ камерам")
            self.set_fw_nat_rule_enable(self.nat_rules)
        if data == "disable_cameras":
            self.logger.log(f"Нажата кнопка Вылючить доступ камерам")
            self.set_fw_nat_rule_disable(self.nat_rules)

    def filter_nat_rules(self, nat_rule_desc):
        try:
            self.nat_rules = []
            fw_nat_rules = json.loads(self.http_session.get_fw_rules().text)["data"]
        except Exception as error:
            return self.alert(*Alerts.cant_connect)
        for id, rule in enumerate(fw_nat_rules):
            if nat_rule_desc in rule["descr"].lower():
                if "disabled" in rule:
                    rule_status = "disabled"
                else:
                    rule_status = "enabled"
                self.nat_rules.append({"id": id, "rule_status": rule_status})

    def connect_to_router(self):
        if not self.http_session:
            self.http_session = HttpHandler(
                self.cf.ipaddress, self.cf.login, self.cf.password
            )
            # self.check_connection()
            self.get_router_status()
            self.get_fw_rule_status()
            check_rule_thread = Thread(target=self.get_fw_rule_status_thread)
            # check_rule_thread.daemon = True
            check_rule_thread.start()
        elif self.get_router_status():
            self.alert(*Alerts.already_connected)
        else:
            self.alert(*Alerts.cant_connect)

        self.gui.update()

    def get_fw_rule_status(self):
        # Включить если надо руками вводить правило

        # if self.gui.nat_rule_desc_input.value == "":
        #     self.nat_rule_desc = self.gui.default_nat_description
        # else:
        #     self.nat_rule_desc = self.gui.nat_rule_desc_input.value
        # self.set_fw_rule_desc(desc=self.nat_rule_desc)
        self.filter_nat_rules(self.nat_rule_desc)
        disabled = [
            x["rule_status"] for x in self.nat_rules if x["rule_status"] == "disabled"
        ]
        if not self.nat_rules or len(self.nat_rules) == 0:
            self.gui.cameras_status_text.value = (
                "Проверьте пункт rule-desc в файле конфигурации"
            )
            self.gui.cameras_status_text.color = colors.RED_500
            self.gui.update()
            return self.alert(*Alerts.no_rules_found)
        if len(disabled) > 0:
            self.gui.cameras_status_text.value = "Выключены"
            self.gui.cameras_status_text.color = colors.RED_400
            self.gui.update()
            return False
        else:
            self.gui.cameras_status_text.value = "Включены"
            self.gui.cameras_status_text.color = colors.GREEN_400
            self.gui.update()
            return True

    def get_router_status(self):
        try:
            response = self.http_session.get_fw_rules()
        except:
            response = None
        if response == None:
            router_status = "Не подключено"
            self.gui.router_status_text.color = colors.RED_400
            self.gui.router_status_text.value = router_status
            self.router_status = False
            return False
        elif response.status_code == 401:
            router_status = "Не верный логин или пароль"
            self.gui.router_status_text.color = colors.RED_400
            self.gui.router_status_text.value = router_status
            self.router_status = False
            self.alert(*Alerts.wrong_login_password)
            return False

        else:
            router_status = "Подключено"
            self.gui.router_status_text.color = colors.GREEN_400
            self.gui.router_status_text.value = router_status
            self.router_status = True
            return True

    # def set_fw_rule_desc(self, desc=None):
    #     return self.gui.default_nat_description

    def set_fw_nat_rule_disable(self, rules):
        if not self.http_session:
            return self.alert(*Alerts.no_session)
        if len(rules) == 0:
            return self.alert(*Alerts.no_rules_found)
        response = self.http_session.set_fw_rules(rules, disable=True)
        try:
            if response[0].status_code == 200:
                self.alert(*Alerts.successfully_disabled)
            else:
                self.alert(f"Запрос неудачен {response.status_code}", colors.RED_500)
                self.logger.log(f"Запрос неудачен {response.status_code}")
        except Exception as error:
            self.alert(f"Запрос неудачен {error}", colors.RED_500)
            self.logger.log(f"Запрос неудачен {response.status_code}")
        self.get_fw_rule_status()
        self.gui.update()
        self.logger.log(f"Правило(а) включены {[x for x in rules]}")

    def set_fw_nat_rule_enable(self, rules):
        if not self.http_session:
            return self.alert(*Alerts.no_session)
        if len(rules) == 0:
            return self.alert(*Alerts.no_rules_found)
        response = self.http_session.set_fw_rules(rules, disable=False)
        try:
            if response[0].status_code == 200:
                self.alert(*Alerts.successfully_enabled)
            else:
                self.alert(f"Запрос неудачен {response.status_code}", colors.RED_500)
                self.logger.log(f"Запрос неудачен {response.status_code}")
        except Exception as error:
            self.alert(f"Запрос неудачен {error}", colors.RED_500)
            self.logger.log(f"Запрос неудачен {response.status_code}")
        self.get_fw_rule_status()
        self.gui.update()
        self.logger.log(f"Правило(а) включены {[x for x in rules]}")

    def alert(self, alert_text, bgcolor):
        self.gui.alert.content = Text(f"{alert_text}", size=20)
        self.gui.alert.bgcolor = bgcolor
        self.gui.alert.open = True
        self.gui.update()

    # Сделать поток с проверкой
    def get_fw_rule_status_thread(self):
        while True:
            if self.router_status:
                self.get_fw_rule_status()
            else:
                self.logger.log("Нет подключения к роутеру")
                pass
            time.sleep(5)  # import time
