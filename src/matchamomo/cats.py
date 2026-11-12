"""ASCII art sprites and Rich styling for the large orange cat and small tortie."""

from __future__ import annotations

from collections.abc import Sequence
from enum import StrEnum

from rich.style import Style
from rich.text import Text


class CatKind(StrEnum):
    """The two cats."""

    ORANGE = "orange"
    TORTIE = "tortie"


class CatPose(StrEnum):
    """Animation poses for the cats."""

    STANDING = "standing"
    RUNNING_RIGHT = "running_right"
    RUNNING_LEFT = "running_left"
    NAPPING = "napping"
    EATING_SNACK = "eating_snack"
    PLAYING_STRING = "playing_string"


ORANGE_STANDING_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_____/\        ",
        r" /  o   o  \       ",
        r"( ==  ^  == )  _   ",
        r" )         (  / \  ",
        r"(   |   |   )/  /  ",
        r"(  (|) (|)  )__/   ",
        r"(__/(___)___)      ",
    ),
    (
        r"  /\_____/\        ",
        r" /  o   o  \    _  ",
        r"( ==  ^  == )  / \ ",
        r" )         (   | | ",
        r"(   |   |   )__/ / ",
        r"(  (|) (|)  )___/  ",
        r"(__/(___)___)      ",
    ),
    (
        r"  /\_____/\        ",
        r" /  -   -  \       ",
        r"( ==  ^  == )  _   ",
        r" )         (  / \  ",
        r"(   |   |   )/  /  ",
        r"(  (|) (|)  )__/   ",
        r"(__/(___)___)      ",
    ),
)

TORTIE_STANDING_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_/\   _  ",
        r" ( o.o ) / \ ",
        r"  > ^ < /  / ",
        r" (  m  )__/  ",
        r" (__)__)     ",
    ),
    (
        r"  /\_/\    _ ",
        r" ( o.o )  / \ ",
        r"  > ^ <  /  /",
        r" (  m  )_/ / ",
        r" (__)__)__/  ",
    ),
    (
        r"  /\_/\   _  ",
        r" ( -.- ) / \ ",
        r"  > ^ < /  / ",
        r" (  m  )__/  ",
        r" (__)__)     ",
    ),
)

ORANGE_RUNNING_RIGHT_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"         /\___/\    ",
        r"  ___   /  o  o \   ",
        r" /   \_(   == ^  )  ",
        r"/       \  ~~~~ /   ",
        r"\_   ___/      \    ",
        r" /  /   \  \ \  \   ",
        r"(__/     (__) (__)  ",
    ),
    (
        r"         /\___/\    ",
        r"   __   /  o  o \   ",
        r"  /  \_(   == ^  )  ",
        r" /      \  ~~~~ /   ",
        r" \______/      /    ",
        r"   /  /  /  / /     ",
        r"  (__/  (__)(_)     ",
    ),
)

ORANGE_RUNNING_LEFT_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"    /\___/\         ",
        r"   / o  o  \   ___  ",
        r"  (  ^ ==   )_/   \ ",
        r"   \ ~~~~  /       \\",
        r"    \      \___   _/",
        r"   /  / /  /   \  \ ",
        r"  (__) (__)     \__)",
    ),
    (
        r"    /\___/\         ",
        r"   / o  o  \   __   ",
        r"  (  ^ ==   )_/  \  ",
        r"   \ ~~~~  /      \ ",
        r"    \      \______/ ",
        r"     \ \  \  \  \   ",
        r"     (_)(__)  \__)  ",
    ),
)

TORTIE_RUNNING_RIGHT_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"      /\_/\  ",
        r" __  ( o.o ) ",
        r"/  \_/  ^  ) ",
        r"\____/  / /  ",
        r" /_/  (_)(_) ",
    ),
    (
        r"      /\_/\  ",
        r"  _  ( o.o ) ",
        r" / \_/  ^  ) ",
        r" \___/  / /  ",
        r"  \_/ (_)/   ",
    ),
)

TORTIE_RUNNING_LEFT_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_/\      ",
        r" ( o.o )  __ ",
        r" (  ^  \_/  \\",
        r"  \ \  \____/",
        r" (_)(_)  \_\ ",
    ),
    (
        r"  /\_/\      ",
        r" ( o.o )  _  ",
        r" (  ^  \_/ \ ",
        r"  \ \  \___/ ",
        r"   \(_) /_/  ",
    ),
)

ORANGE_NAPPING_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"    /\___/\        ",
        r"   / -   - \  ___  ",
        r"  ( ==  ^  ==/   \ ",
        r"  /   ~~~~       / ",
        r" (______________/  ",
    ),
    (
        r"    /\___/\        ",
        r"   / -   - \  ____ ",
        r"  ( ==  ^  ==/    \\",
        r"  /   ~~~~        /",
        r" (_______________/ ",
    ),
)

TORTIE_NAPPING_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_/\     ",
        r" ( -.- )__  ",
        r" /  ^     \ ",
        r"(_________/ ",
    ),
    (
        r"  /\_/\     ",
        r" ( -.- )___ ",
        r" /  ^      \\",
        r"(__________/ ",
    ),
)

ORANGE_EATING_SNACK_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_____/\             ",
        r" /  ^   ^  \            ",
        r"( ==  w  == )           ",
        r" )         (____        ",
        r"(   |   |   )   \  ___  ",
        r"(  (|) (|)  )____\/***\ ",
        r"(__/(___)___)     \___/ ",
    ),
    (
        r"  /\_____/\             ",
        r" /  -   -  \            ",
        r"( ==  o  == )           ",
        r" )         (____        ",
        r"(   |   |   )   \  ___  ",
        r"(  (|) (|)  )____\/.*.\ ",
        r"(__/(___)___)     \___/ ",
    ),
)

TORTIE_PLAYING_STRING_FRAMES: tuple[tuple[str, ...], ...] = (
    (
        r"  /\_/\    ~|   ",
        r" ( o.o ) _/ *   ",
        r"  > ^ < /       ",
        r" (  m  )___     ",
        r" (__)__)___)    ",
    ),
    (
        r"  /\_/\     |~  ",
        r" ( o.o )  \_*   ",
        r"  > ^ <  /      ",
        r" (  m  )___     ",
        r" (__)__)___)    ",
    ),
)

SPRITE_MAP: dict[tuple[CatKind, CatPose], tuple[tuple[str, ...], ...]] = {
    (CatKind.ORANGE, CatPose.STANDING): ORANGE_STANDING_FRAMES,
    (CatKind.ORANGE, CatPose.RUNNING_RIGHT): ORANGE_RUNNING_RIGHT_FRAMES,
    (CatKind.ORANGE, CatPose.RUNNING_LEFT): ORANGE_RUNNING_LEFT_FRAMES,
    (CatKind.ORANGE, CatPose.NAPPING): ORANGE_NAPPING_FRAMES,
    (CatKind.ORANGE, CatPose.EATING_SNACK): ORANGE_EATING_SNACK_FRAMES,
    (CatKind.TORTIE, CatPose.STANDING): TORTIE_STANDING_FRAMES,
    (CatKind.TORTIE, CatPose.RUNNING_RIGHT): TORTIE_RUNNING_RIGHT_FRAMES,
    (CatKind.TORTIE, CatPose.RUNNING_LEFT): TORTIE_RUNNING_LEFT_FRAMES,
    (CatKind.TORTIE, CatPose.NAPPING): TORTIE_NAPPING_FRAMES,
    (CatKind.TORTIE, CatPose.PLAYING_STRING): TORTIE_PLAYING_STRING_FRAMES,
}

_ORANGE_BODY = Style(color="#FF8C00", bold=True)
_ORANGE_STRIPE = Style(color="#CC5500", bold=True)
_ORANGE_NOSE = Style(color="#FF85A1", bold=True)
_ORANGE_EYE = Style(color="#FFF3B0", bold=True)

_TORTIE_PALETTE = (
    Style(color="#8B5A2B", bold=True),  # warm dark brown
    Style(color="#E07A22", bold=True),  # ginger patch
    Style(color="#F4D06F", bold=True),  # cream fleck
    Style(color="#78716C", bold=True),  # charcoal/slate
)
_TORTIE_NOSE = Style(color="#FF99AA", bold=True)
_TORTIE_EYE = Style(color="#A3E635", bold=True)


def get_sprite(kind: CatKind, pose: CatPose, frame_index: int = 0) -> tuple[str, ...]:
    """Return a normalized rectangular ASCII sprite for the given cat, pose, and frame."""
    frames = SPRITE_MAP[(kind, pose)]
    raw = frames[frame_index % len(frames)]
    width = max(len(line) for line in raw)
    return tuple(line.ljust(width) for line in raw)


def style_sprite_line(kind: CatKind, line: str, row_idx: int) -> Text:
    """Apply cat-appropriate colors to a single line of a sprite."""
    styled = Text()
    if kind == CatKind.ORANGE:
        for _col_idx, ch in enumerate(line):
            if ch == " ":
                styled.append(ch)
            elif ch == "^":
                styled.append(ch, style=_ORANGE_NOSE)
            elif ch in ("o", "O"):
                styled.append(ch, style=_ORANGE_EYE)
            elif ch in ("~", "=", "|") or (row_idx == 0 and ch == "_"):
                styled.append(ch, style=_ORANGE_STRIPE)
            else:
                styled.append(ch, style=_ORANGE_BODY)
        return styled

    # Tortoiseshell mottled pattern
    for col_idx, ch in enumerate(line):
        if ch == " ":
            styled.append(ch)
        elif ch == "^":
            styled.append(ch, style=_TORTIE_NOSE)
        elif ch in ("o", "O"):
            styled.append(ch, style=_TORTIE_EYE)
        else:
            patch_idx = (row_idx * 3 + col_idx // 2) % len(_TORTIE_PALETTE)
            styled.append(ch, style=_TORTIE_PALETTE[patch_idx])
    return styled


def pad_sprite_top(lines: Sequence[str], target_height: int) -> list[str]:
    """Pad a sprite with blank lines at the top so its feet align to ``target_height``."""
    if len(lines) >= target_height:
        return list(lines)
    width = len(lines[0]) if lines else 0
    padding = [" " * width for _ in range(target_height - len(lines))]
    return padding + list(lines)
