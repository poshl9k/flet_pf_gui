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
    TextField,
    WEB_BROWSER,
    AppBar,
    PopupMenuItem,
    PopupMenuButton,
)

# from ui import
from utils import ScreenRes
from event_handler import EventHandler

VERSION = "v 0.1"
SCREEN_RESOLUTION = ScreenRes().resolution


class PfsenseApiApp(UserControl):
    def build(self):
        self.eh = EventHandler(self)
        self.cameras_status_text = Text(
            "Статус неизвестен, нет подключения", size=25, color=colors.AMBER_300
        )
        self.router_status_text = Text("")
        
        # Alert instance
        self.alert = SnackBar(content=Text(""))
        self.default_nat_description = "miha-m-from-home"
        self.nat_rule_desc_input = TextField(
            border_color=colors.WHITE12,
            bgcolor=colors.WHITE24,
            label="Введите сюда описание правила (как на роутере)",
            hint_text=f"пример - {self.default_nat_description}",
        )
        self.first_row = Container(
            content=Row(
                controls=[
                    Text(f"Видеокамеры ЦОК сейчас", size=25),
                    self.cameras_status_text,
                    # self.nat_rule_desc_input,
                ],
                wrap=True,
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
        self.secont_row_second_column = Column(
            controls=[
                Text(value="Статус подключения к роутеру:", size=15, text_align=TextAlign.START),
                self.router_status_text,
            ]
        )
        self.second_row = Container(
            content=Row(
                controls=[self.second_row_first_column, self.secont_row_second_column],
            ),
            padding=5,
            margin=margin.all(1),
        )
        self.third_row_column = Column(
            # width=300,
            controls=[
                ElevatedButton(
                    # width=300,
                    data="enable_cameras",
                    on_click=self.button_clicked,
                    height=150,
                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=2)),
                    content=Row(
                        controls=[
                            Icon(
                                name=icons.PHOTO_CAMERA_OUTLINED,
                                size=45,
                                color=colors.GREEN_500,
                            ),
                            Text(value="Включить доступ к камерам", size=25),
                        ],
                    ),
                ),
            ],
        )
        self.third_row = Container(
            content=Row(
                expand=True,
                controls=[self.third_row_column],
            ),
            padding=5,
            margin=margin.all(1),
        )
        self.fourth_row_column = Column(
            # width=300,
            controls=[
                ElevatedButton(
                    # width=300,
                    data="disable_cameras",
                    on_click=self.button_clicked,
                    height=150,
                    style=ButtonStyle(shape=RoundedRectangleBorder(radius=2)),
                    content=Row(
                        controls=[
                            Icon(
                                name=icons.PHOTO_CAMERA_OUTLINED,
                                size=45,
                                color=colors.RED_500,
                            ),
                            Text(value="Выключить доступ к камерам", size=25),
                        ],
                    ),
                )
            ],
        )
        self.fourth_row = Container(
            content=Row(
                expand=True,
                controls=[self.fourth_row_column],
            ),
            padding=5,
            margin=margin.all(1),
        )

        self.layout = [
            Column(
                controls=[
                    self.first_row,
                    Divider(height=3),
                    self.second_row,
                    self.third_row,
                    self.fourth_row,
                    self.alert,
                ]
            )
        ]
        return self.layout

    def button_clicked(self, e):
        self.eh.handle_event(e)
        pass

    def page_resize(self, e):
        print("New page size:", self.page.window_width, self.page.window_height)
        self.fourth_row_column.controls[0].width = self.page.window_width - 50
        self.third_row_column.controls[0].width = self.page.window_width - 50
        for control in self.second_row.content.controls:
            control.width = (self.page.window_width / 2) - 50 / 2
        self.update()


def main(page: Page):
    
    # page.appbar = AppBar(
    #         leading=Icon(icons.PALETTE),
    #         leading_width=40,
    #         title=Text("AppBar Example"),
    #         center_title=False,
    #         bgcolor=colors.SURFACE_VARIANT,
    #         actions=[
    #             IconButton(icons.WB_SUNNY_OUTLINED),
    #             IconButton(icons.FILTER_3),
    #             PopupMenuButton(
    #                 items=[
    #                     PopupMenuItem(text="Item 1"),
    #                     PopupMenuItem(),  # divider
    #                 ]
    #             ),
    #         ],
    #     )
    page.title = f"Управление ВидеоКамерами {VERSION}"
    page.window_min_width = 800
    page.window_min_height = 700
    page.window_max_width = SCREEN_RESOLUTION[0]
    page.window_max_height = SCREEN_RESOLUTION[1]
    page.window_width = page.window_min_width
    page.window_height = page.window_min_height
    page.scale = Scale(scale=8.0)
    pfapi = PfsenseApiApp()
    # add application's root control to the page
    page.on_resize = pfapi.page_resize

    page.add(pfapi)
    


flet.app(target=main)
