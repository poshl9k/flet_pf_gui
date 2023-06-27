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


class EventHandler:
    """
    gui:PfsenseApiApp
    """

    def __init__(self, gui) -> None:
        self.gui = gui
        self.http_session = None
        self.nat_rules = list()
        self.nat_rule_desc = ""

    def handle_event(self, event):
        data = event.control.data
        if data == "Connect_to_router":
            self.connect_to_router()
            # gui.cameras_status_text.value = "12344"
            self.gui.update()
        if data == "enable_cameras":
            self.set_fw_nat_rule_enable(self.nat_rules)

    def filter_nat_rules(self, nat_rule_desc):
        fw_nat_rules = json.loads(self.http_session.get_fw_rules().text)["data"]
        for id, rule in enumerate(fw_nat_rules):
            if nat_rule_desc in rule["descr"]:
                if "disabled" in rule:
                    rule_status = "disabled"
                else:
                    rule_status = "enabled"
                self.nat_rules.append({"id": id, "rule_status": rule_status})

    def connect_to_router(self):
        if not self.http_session:
            self.http_session = HttpHandler("192.168.10.8", "admin", "123qwe123***")
            self.get_router_status()
            self.get_fw_rule_status()
        else:
            self.gui.alert.content = Text("Уже подключено!")
            self.gui.alert.open = True
            self.gui.alert.bgcolor = colors.GREEN_400
            self.gui.update()

    def get_fw_rule_status(self):
        if self.gui.nat_rule_desc_input.value == "":
            self.nat_rule_desc = self.gui.default_nat_description
        else:
            self.nat_rule_desc = self.gui.nat_rule_desc_input.value
        self.set_fw_rule_desc(desc=self.nat_rule_desc)
        self.filter_nat_rules(self.nat_rule_desc)
        disabled = [
            x["rule_status"] for x in self.nat_rules if x["rule_status"] == "disabled"
        ]
        if len(disabled) > 0:
            self.gui.cameras_status_text.value = "Выключены"
            self.gui.cameras_status_text.color = colors.RED_400
        else:
            self.gui.cameras_status_text.value = "Включены"
            self.gui.cameras_status_text.color = colors.GREEN_400

    def get_router_status(self):
        """
        Purpose: self
        """
        if self.http_session == None:
            router_status = "Не подключено"
            self.gui.router_status.color = colors.RED_400
        else:
            router_status = "Подключено"
            self.gui.router_status.color = colors.GREEN_400
        self.gui.router_status.value = router_status

    def set_fw_rule_desc(self, desc=None):
        return self.gui.default_nat_description

    def set_fw_nat_rule_disable(self, rules):
        response = self.http_session.set_fw_rules(rules, disable=False)

    def set_fw_nat_rule_enable(self, rules):
        response = self.http_session.set_fw_rules(rules, disable=True)
