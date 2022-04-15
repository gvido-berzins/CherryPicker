import textwrap
from dataclasses import dataclass


@dataclass
class Codebox:
    idx: int
    txt: str
    node_name: str

    def __str__(self) -> str:
        short_txt = textwrap.shorten(self.txt, 40)
        short_node_name = textwrap.shorten(self.node_name, 25)
        return f"{self.idx:<5}) {short_node_name:<26}: {short_txt!r}"
