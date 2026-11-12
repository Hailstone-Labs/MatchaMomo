"""Unit tests for cat ASCII sprites and styling."""

from matchamomo.cats import (
    SPRITE_MAP,
    CatKind,
    CatPose,
    get_sprite,
    pad_sprite_top,
    style_sprite_line,
)


def test_all_sprites_rectangular_and_nonempty() -> None:
    for (kind, pose), frames in SPRITE_MAP.items():
        assert len(frames) >= 2
        for idx in range(len(frames)):
            sprite = get_sprite(kind, pose, idx)
            assert len(sprite) > 0
            widths = {len(line) for line in sprite}
            assert len(widths) == 1
            assert next(iter(widths)) > 0


def test_orange_cat_larger_than_tortie() -> None:
    shared_poses = (
        CatPose.STANDING,
        CatPose.RUNNING_RIGHT,
        CatPose.RUNNING_LEFT,
        CatPose.NAPPING,
    )
    for pose in shared_poses:
        orange = get_sprite(CatKind.ORANGE, pose, 0)
        tortie = get_sprite(CatKind.TORTIE, pose, 0)
        assert len(orange) > len(tortie)
        assert len(orange[0]) > len(tortie[0])

    orange_snack = get_sprite(CatKind.ORANGE, CatPose.EATING_SNACK, 0)
    tortie_string = get_sprite(CatKind.TORTIE, CatPose.PLAYING_STRING, 0)
    assert len(orange_snack) > len(tortie_string)
    assert len(orange_snack[0]) > len(tortie_string[0])


def test_style_sprite_line_preserves_text() -> None:
    sprite = get_sprite(CatKind.TORTIE, CatPose.STANDING, 0)
    for row_idx, line in enumerate(sprite):
        styled = style_sprite_line(CatKind.TORTIE, line, row_idx)
        assert styled.plain == line


def test_pad_sprite_top_aligns_height() -> None:
    tortie = get_sprite(CatKind.TORTIE, CatPose.STANDING, 0)
    padded = pad_sprite_top(tortie, 7)
    assert len(padded) == 7
    assert padded[-len(tortie) :] == list(tortie)
