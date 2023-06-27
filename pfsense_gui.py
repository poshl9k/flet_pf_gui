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
)

# from ui import
from utils import ScreenRes
from event_handler import EventHandler as eh

VERSION = "v 0.1"
SCREEN_RESOLUTION = ScreenRes().resolution


class PfsenseApiApp(UserControl):
    def build(self):
        self.status_text = Text("Выключены", size=25, color=colors.RED_300)

        self.first_row = Container(
            content=Row(
                controls=[
                    Text(f"Видеокамеры ЦОК сейчас", size=25),
                    self.status_text,
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
        self.secont_row_second_column = Column(
            controls=[
                Text(value="Статус подключения:", size=15, text_align=TextAlign.START),
                self.router_status(),
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
                ]
            )
        ]
        return self.layout

    def router_status(self, api=None):
        """
        Purpose: self
        """
        router_status = "Не подключено"
        return Text(
            value=f"{router_status}",
            size=25,
            text_align=TextAlign.CENTER,
        )

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
