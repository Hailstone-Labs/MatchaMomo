"""Animated ASCII cat stage widget for MatchaMomo."""

from __future__ import annotations

from enum import StrEnum

from rich.style import Style
from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget

from matchamomo.cats import (
    CatKind,
    CatPose,
    get_sprite,
    pad_sprite_top,
    style_sprite_line,
)


class StageMode(StrEnum):
    """Visual animation mode for the two cats."""

    STANDING = "standing"
    CHASING = "chasing"
    NAPPING = "napping"
    LONG_BREAK = "long_break"


_GROUND_STYLE = Style(color="#57534E")
_DUST_STYLE = Style(color="#A8A29E", dim=True)
_ZZZ_STYLE = Style(color="#93C5FD", bold=True)
_SNACK_STYLE = Style(color="#FCD34D", bold=True)
_STRING_STYLE = Style(color="#F472B6", bold=True)

STAGE_SPRITE_HEIGHT = 9  # 2 sky/zzz rows + 7 cat rows


class CatStage(Widget):
    """Renders the large orange cat and small tortie in standing, chasing, or napping scenes."""

    mode: reactive[StageMode] = reactive(StageMode.STANDING)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._tick_count: int = 0
        self._chase_x: int = 4
        self._chase_dir: int = 1  # 1 = right, -1 = left
        self._lap_count: int = 0

    def on_mount(self) -> None:
        """Start the animation loop."""
        self.set_interval(0.18, self._advance_animation)

    def watch_mode(self, new_mode: StageMode) -> None:
        """Reset chase position when entering chasing mode and refresh."""
        if new_mode == StageMode.CHASING:
            self._chase_x = 2
            self._chase_dir = 1
        self.refresh()

    def _advance_animation(self) -> None:
        self._tick_count += 1
        if self.mode == StageMode.CHASING:
            stage_width = max(48, self.size.width or 72)
            group_width = 40  # orange + gap + tortie
            max_x = max(2, stage_width - group_width - 2)
            step = 3
            self._chase_x += step * self._chase_dir
            if self._chase_x >= max_x:
                self._chase_x = max_x
                self._chase_dir = -1
                self._lap_count += 1
            elif self._chase_x <= 2:
                self._chase_x = 2
                self._chase_dir = 1
                self._lap_count += 1
        self.refresh()

    def render(self) -> Text:
        """Render the current scene as a Rich Text block."""
        width = max(48, self.size.width or 72)
        if self.mode == StageMode.CHASING:
            return self._render_chasing(width)
        if self.mode == StageMode.NAPPING:
            return self._render_napping(width)
        if self.mode == StageMode.LONG_BREAK:
            return self._render_long_break(width)
        return self._render_standing(width)

    def _render_standing(self, width: int) -> Text:
        # Subtle idle animation: mostly frame 0, occasional tail wag (1) or blink (2)
        cycle = self._tick_count % 24
        if cycle in (8, 9, 10):
            frame_idx = 1
        elif cycle == 18:
            frame_idx = 2
        else:
            frame_idx = 0

        orange = pad_sprite_top(get_sprite(CatKind.ORANGE, CatPose.STANDING, frame_idx), 7)
        tortie = pad_sprite_top(get_sprite(CatKind.TORTIE, CatPose.STANDING, frame_idx), 7)

        gap = 3
        total_w = len(orange[0]) + gap + len(tortie[0])
        left_pad = max(0, (width - total_w) // 2)

        output = Text()
        # 2 sky rows for consistent stage height
        output.append("\n\n")
        for row_idx in range(7):
            output.append(" " * left_pad)
            output.append_text(style_sprite_line(CatKind.ORANGE, orange[row_idx], row_idx))
            output.append(" " * gap)
            output.append_text(style_sprite_line(CatKind.TORTIE, tortie[row_idx], row_idx))
            output.append("\n")

        output.append(self._ground_line(width))
        return output

    def _render_chasing(self, width: int) -> Text:
        frame_idx = self._tick_count % 2
        pose = CatPose.RUNNING_RIGHT if self._chase_dir == 1 else CatPose.RUNNING_LEFT

        orange = pad_sprite_top(get_sprite(CatKind.ORANGE, pose, frame_idx), 7)
        tortie = pad_sprite_top(get_sprite(CatKind.TORTIE, pose, frame_idx), 7)

        gap = 3
        orange_first = (
            (self._lap_count % 2 == 0) if self._chase_dir == -1 else (self._lap_count % 2 == 1)
        )
        if self._chase_dir == 1:
            # Running right: leader is on the right, chaser on the left
            left_cat, left_kind = (
                (tortie, CatKind.TORTIE) if orange_first else (orange, CatKind.ORANGE)
            )
            right_cat, right_kind = (
                (orange, CatKind.ORANGE) if orange_first else (tortie, CatKind.TORTIE)
            )
        else:
            # Running left: leader is on the left, chaser on the right
            left_cat, left_kind = (
                (orange, CatKind.ORANGE) if orange_first else (tortie, CatKind.TORTIE)
            )
            right_cat, right_kind = (
                (tortie, CatKind.TORTIE) if orange_first else (orange, CatKind.ORANGE)
            )

        total_w = len(left_cat[0]) + gap + len(right_cat[0])
        x = max(1, min(self._chase_x, max(1, width - total_w - 2)))

        dust_chars = ("·", "•", "*")
        dust = dust_chars[self._tick_count % len(dust_chars)]

        output = Text()
        output.append("\n\n")
        for row_idx in range(7):
            line = Text()
            if row_idx == 6 and self._chase_dir == 1 and x >= 3:
                line.append(" " * (x - 3))
                line.append(f"{dust} ~", style=_DUST_STYLE)
            else:
                line.append(" " * x)

            line.append_text(style_sprite_line(left_kind, left_cat[row_idx], row_idx))
            line.append(" " * gap)
            line.append_text(style_sprite_line(right_kind, right_cat[row_idx], row_idx))

            if row_idx == 6 and self._chase_dir == -1 and x + total_w + 3 < width:
                line.append(f"~ {dust}", style=_DUST_STYLE)

            output.append_text(line)
            output.append("\n")

        output.append(self._ground_line(width))
        return output

    def _render_napping(self, width: int) -> Text:
        # Slow gentle breathing cycle
        frame_idx = (self._tick_count // 5) % 2
        orange = pad_sprite_top(get_sprite(CatKind.ORANGE, CatPose.NAPPING, frame_idx), 7)
        tortie = pad_sprite_top(get_sprite(CatKind.TORTIE, CatPose.NAPPING, frame_idx), 7)

        gap = 3
        total_w = len(orange[0]) + gap + len(tortie[0])
        left_pad = max(0, (width - total_w) // 2)

        zzz_step = (self._tick_count // 3) % 4
        z_top = "      Z        z" if zzz_step in (2, 3) else "     z          "
        z_mid = "   z   Z      Z " if zzz_step in (1, 2) else "  z          z  "

        output = Text()
        output.append(" " * (left_pad + 6))
        output.append(z_top, style=_ZZZ_STYLE)
        output.append("\n")
        output.append(" " * (left_pad + 5))
        output.append(z_mid, style=_ZZZ_STYLE)
        output.append("\n")

        for row_idx in range(7):
            output.append(" " * left_pad)
            output.append_text(style_sprite_line(CatKind.ORANGE, orange[row_idx], row_idx))
            output.append(" " * gap)
            output.append_text(style_sprite_line(CatKind.TORTIE, tortie[row_idx], row_idx))
            output.append("\n")

        output.append(self._ground_line(width))
        return output

    def _render_long_break(self, width: int) -> Text:
        frame_idx = (self._tick_count // 3) % 2
        orange = pad_sprite_top(get_sprite(CatKind.ORANGE, CatPose.EATING_SNACK, frame_idx), 7)
        tortie = pad_sprite_top(get_sprite(CatKind.TORTIE, CatPose.PLAYING_STRING, frame_idx), 7)

        gap = 4
        total_w = len(orange[0]) + gap + len(tortie[0])
        left_pad = max(0, (width - total_w) // 2)

        nom_label = "*nom nom*" if frame_idx == 0 else "  *munch*"
        string_top = "  | " if frame_idx == 0 else "   |"
        string_mid = "  ~ " if frame_idx == 0 else "  S "

        output = Text()
        # Sky row 0: dangling string above tortie
        output.append(" " * (left_pad + len(orange[0]) + gap + 9))
        output.append(string_top, style=_STRING_STYLE)
        output.append("\n")

        # Sky row 1: *nom* over orange snack + dangling string over tortie
        output.append(" " * (left_pad + 14))
        output.append(nom_label, style=_SNACK_STYLE)
        output.append(" " * (len(orange[0]) - 14 - len(nom_label) + gap + 9))
        output.append(string_mid, style=_STRING_STYLE)
        output.append("\n")

        for row_idx in range(7):
            output.append(" " * left_pad)
            output.append_text(style_sprite_line(CatKind.ORANGE, orange[row_idx], row_idx))
            output.append(" " * gap)
            output.append_text(style_sprite_line(CatKind.TORTIE, tortie[row_idx], row_idx))
            output.append("\n")

        output.append(self._ground_line(width))
        return output

    @staticmethod
    def _ground_line(width: int) -> Text:
        line_str = "─" * max(20, width - 4)
        pad = max(0, (width - len(line_str)) // 2)
        t = Text()
        t.append(" " * pad)
        t.append(line_str, style=_GROUND_STYLE)
        return t
