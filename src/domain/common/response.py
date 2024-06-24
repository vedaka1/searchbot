from dataclasses import dataclass, field


@dataclass
class Response:
    value: str
    _symbols_to_ignore: str = field(default=r"_*[]()~`>#+-=|{}.!", init=False)

    def __post_init__(self):
        for symbol in self._symbols_to_ignore:
            self.value = self.value.replace(symbol, f"\{symbol}")
        self.value = self.value.replace(r"\*", "*")
