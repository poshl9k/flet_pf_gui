import flet
from flet import (
    colors,
)


class Alerts:
    no_session = ("Нет подлючения к роутеру, сначала подключитесь",colors.AMBER_400)
    cant_connect = ("Не возможно подключиться к роутеру, проверьте подключение и адрес роутера ", colors.RED_400)
    already_connected = ("Уже подключено!",colors.GREEN_400)
    successfully_enabled = ("Доступ успешно включен",colors.GREEN_400)
    successfully_disabled = ("Доступ успешно выключен",colors.GREEN_400)
