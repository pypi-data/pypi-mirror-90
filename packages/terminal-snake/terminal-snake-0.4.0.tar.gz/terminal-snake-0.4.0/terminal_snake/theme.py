from dataclasses import dataclass, field


def tail_factory():
    default = {  # left, right, up, down (start → end)
        "rl": "━",
        "lr": "━",
        "ud": "┃",
        "du": "┃",
        "rd": "┏",
        "dr": "┏",
        "ru": "┗",
        "ur": "┗",
        "ld": "┓",
        "dl": "┓",
        "lu": "┛",
        "ul": "┛",
    }
    return default


@dataclass
class Theme:
    border_piece: str = "🟧"
    field_piece: str = "🟫"
    apple: str = "🍎"
    head: str = "😳"
    tail_end: str = "•"
    tail: dict = field(default_factory=tail_factory)
    character_separator: str = "\t"


LineTheme = Theme()
DefaultTheme = Theme(tail_end="🔲", character_separator="",
                     tail={"rl": "🔲", "lr": "🔲", "ud": "🔲", "du": "🔲", "rd": "🔲", "dr": "🔲",
                           "ru": "🔲", "ur": "🔲", "ld": "🔲", "dl": "🔲", "lu": "🔲", "ul": "🔲", })
