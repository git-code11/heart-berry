from enum import Enum
from dataclasses import dataclass
from functools import partial

from kivy.utils import get_color_from_hex

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.graphics import Color


@dataclass
class StatusColor:
    bg: str
    text: str

    def __getattribute__(self, name: str):
        hex_value = object.__getattribute__(self, name)
        return get_color_from_hex(hex_value)


status_color_map = dict(
    error=StatusColor("#FFBABA", "#D8000C"),
    warn=StatusColor("#FEEFB3", "#9F6000"),
    success=StatusColor("#4F8A10", "#DFF2BF"),
    info=StatusColor("#D9EDF7", "#31708F")
)


class StatusKind(Enum):
    ERROR = "error"
    WARN = "Warn"
    SUCCESS = "success"
    INFO = "info"
    LOADING = "loading"
    IDLE = "idle"

    def transform(self):
        return self.name.lower()


class StatusSnackBar:
    def create(self,
               text: str,
               text_color: Color | str,
               bg_color: Color | str,
               **kwargs) -> MDSnackbar:
        prop = dict(
            y="24dp",
            pos_hint={"center_x": 0.5},
            size_hint_x=.75,
            duration=1.5,
            background_color=bg_color
        )
        prop.update(kwargs)

        return MDSnackbar(
            MDSnackbarText(
                text=text,
                theme_text_color="Custom",
                text_color=text_color
            ),
            **prop
        )

    def from_status(self, status: str | StatusKind):
        return getattr(self,
                       status if type(status) is str
                       else status.transform())

    def __getattr__(self, status: str):
        color = status_color_map.get(
            status, status_color_map["info"])
        return partial(self.create,
                       text_color=color.text,
                       bg_color=color.bg)
