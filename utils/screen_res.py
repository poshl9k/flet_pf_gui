from screeninfo import get_monitors


class ScreenRes():
    
    resolution = ()
    
    def __init__(self) -> None:
        mon = get_monitors()
        self.resolution = (mon[0].width,mon[0].height)
            


