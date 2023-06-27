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

from pfsense_gui import PfsenseApiApp as PfApp

class EventHandler:
    """
    gui:PfsenseApiApp
    """

    def handle_event(self, gui: PfApp, event):
        data = event.control.data
        if data == "Connect_to_router":
            self.connect_to_router(gui)
            # gui.cameras_status_text.value = "12344"
            gui.update()

    def connect_to_router(self, gui):
        if not gui.http_session:
            gui.http_session = HttpHandler("192.168.10.8", "admin", "123qwe123***")
            gui.get_router_status()
        else:
            gui.alert.content = Text("Уже подключено!")
            gui.alert.open = True
            gui.alert.bgcolor = colors.GREEN_400
            gui.update()

    def get_fw_rule_status(self, gui):
        gui.http_session.get_fw_rules()
        self.cameras_status_text
