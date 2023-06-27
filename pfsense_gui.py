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

# from ui import
from utils import ScreenRes
from event_handler import EventHandler as eh
from httphandler import HttpHandler

VERSION = "v 0.1"
SCREEN_RESOLUTION = ScreenRes().resolution


class PfsenseApiApp(UserControl):
    def build(self):
        self.http_session = None

        self.cameras_status_text = Text("Статус неизвестен, нет подключения", size=25, color=colors.RED_300)
        self.router_status = Text("")
        # Alert instance
        self.alert = SnackBar(content=Text(""))

        self.first_row = Container(
            content=Row(
                controls=[
                    Text(f"Видеокамеры ЦОК сейчас", size=25),
                    self.cameras_status_text,
                ]
            ),
            padding=5,
            margin=margin.all(1),
        )
        self.second_row_first_column = Column(
            # width=300,
            controls=[
                ElevatedButton(
                    # width=300,
                    data="Connect_to_router",
                    on_click=self.button_clicked,
                    height=150,
                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=2)),
                    content=Row(
                        controls=[
                            Icon(name=icons.CONNECTED_TV, size=25),
                            Text(value="Соединиться с роутером", size=25),
                        ],
                    ),
                ),
            ],
        )
        self.get_router_status()
        self.secont_row_second_column = Column(
            controls=[
                Text(value="Статус подключения:", size=15, text_align=TextAlign.START),
                self.router_status,
            ]
        )
        self.second_row = Container(
            content=Row(
                controls=[self.second_row_first_column, self.secont_row_second_column],
            ),
            padding=5,
            margin=margin.all(1),
        )
        self.divider_row = Row(controls=[Divider(height=5)])

        self.layout = [
            Column(
                controls=[
                    self.first_row,
                    self.second_row,
                    self.alert,
                ]
            )
        ]
        return self.layout

    def get_router_status(self):
        """
        Purpose: self
        """
        if self.http_session == None:
            router_status = "Не подключено"
            self.router_status.color = colors.RED_400
        else:
            router_status = "Подключено"
            self.router_status.color = colors.GREEN_400
        self.router_status.value = router_status

    def button_clicked(self, e):
        eh().handle_event(self, e)


def main(page: Page):
    page.title = f"Управление ВидеоКамерами {VERSION}"
    page.window_min_width = 800
    page.window_min_height = 600
    page.window_max_width = SCREEN_RESOLUTION[0]
    page.window_max_height = SCREEN_RESOLUTION[1]
    page.window_width = page.window_min_width
    page.window_height = page.window_min_height
    page.scale = Scale(scale=8.0)
    pfapi = PfsenseApiApp()

    # add application's root control to the page
    page.add(pfapi)


flet.app(target=main)
