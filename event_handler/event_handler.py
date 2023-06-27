from flet import UserControl


class EventHandler:
    def handle_event(self, gui: UserControl, event):
        pass
        data = event.control.data
        gui.status_text.value = "12344"
        gui.update()
        
