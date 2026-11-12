"""End-to-end headless TUI tests for MatchaMomoApp."""

import pytest
from textual.widgets import Input, Static

from matchamomo.app import MatchaMomoApp
from matchamomo.stage import CatStage, StageMode
from matchamomo.timer import TimerPhase


@pytest.mark.asyncio
async def test_app_startup_cats_standing_together() -> None:
    app = MatchaMomoApp(focus_minutes=20, rest_minutes=5)
    async with app.run_test() as pilot:
        await pilot.pause()
        stage = app.query_one("#cat-stage", CatStage)
        assert stage.mode == StageMode.STANDING
        assert app.timer.phase == TimerPhase.IDLE
        readout = app.query_one("#timer-readout", Static)
        assert "20:00" in str(readout.render())


@pytest.mark.asyncio
async def test_app_start_chasing_and_rest_napping() -> None:
    app = MatchaMomoApp(focus_minutes=15, rest_minutes=4)
    async with app.run_test() as pilot:
        await pilot.pause()
        stage = app.query_one("#cat-stage", CatStage)
        assert stage.mode == StageMode.STANDING

        # Start focus timer -> cats chase each other
        await pilot.press("space")
        await pilot.pause()
        assert app.timer.phase == TimerPhase.FOCUS
        assert app.timer.running is True
        assert stage.mode == StageMode.CHASING

        # Stop focus to rest -> both cats nap
        await pilot.press("n")
        await pilot.pause()
        assert app.timer.phase == TimerPhase.REST
        assert app.timer.running is True
        assert stage.mode == StageMode.NAPPING
        assert "04:00" in str(app.query_one("#timer-readout", Static).render())

        # Reset -> back to standing together
        await pilot.press("r")
        await pilot.pause()
        assert app.timer.phase == TimerPhase.IDLE
        assert stage.mode == StageMode.STANDING


@pytest.mark.asyncio
async def test_app_configure_minutes_modal() -> None:
    app = MatchaMomoApp(focus_minutes=25, rest_minutes=5)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("c")
        await pilot.pause()

        focus_input = app.screen.query_one("#focus-input", Input)
        rest_input = app.screen.query_one("#rest-input", Input)
        long_rest_input = app.screen.query_one("#long-rest-input", Input)
        interval_input = app.screen.query_one("#interval-input", Input)
        focus_input.value = "35"
        rest_input.value = "10"
        long_rest_input.value = "20"
        interval_input.value = "3"

        await pilot.click("#save-config")
        await pilot.pause()

        assert app.timer.focus_minutes == 35
        assert app.timer.rest_minutes == 10
        assert app.timer.long_rest_minutes == 20
        assert app.timer.long_rest_interval == 3
        assert "35:00" in str(app.query_one("#timer-readout", Static).render())


@pytest.mark.asyncio
async def test_app_long_rest_snack_and_string() -> None:
    app = MatchaMomoApp(
        focus_minutes=1,
        rest_minutes=1,
        long_rest_minutes=15,
        long_rest_interval=2,
    )
    async with app.run_test() as pilot:
        await pilot.pause()
        # 1st pomodoro -> regular rest (napping)
        await pilot.press("space")
        app.timer.remaining_seconds = 1
        app._on_second_tick()
        await pilot.pause()
        assert app.timer.phase == TimerPhase.REST
        assert app.query_one("#cat-stage", CatStage).mode == StageMode.NAPPING

        # Finish regular rest -> idle
        app.timer.remaining_seconds = 1
        app._on_second_tick()
        await pilot.pause()
        assert app.timer.phase == TimerPhase.IDLE

        # 2nd pomodoro -> long rest (orange eats snack, tortie plays with string)
        await pilot.press("space")
        app.timer.remaining_seconds = 1
        app._on_second_tick()
        await pilot.pause()

        stage = app.query_one("#cat-stage", CatStage)
        assert app.timer.phase == TimerPhase.LONG_REST
        assert app.timer.completed_pomodoros == 2
        assert stage.mode == StageMode.LONG_BREAK
        assert "15:00" in str(app.query_one("#timer-readout", Static).render())
        assert "nom" in stage.render().plain


@pytest.mark.asyncio
async def test_app_focus_completion_transitions_to_napping() -> None:
    app = MatchaMomoApp(focus_minutes=1, rest_minutes=2)
    async with app.run_test() as pilot:
        await pilot.pause()
        await pilot.press("space")
        await pilot.pause()
        assert app.query_one("#cat-stage", CatStage).mode == StageMode.CHASING

        # Simulate remaining 1 second and one tick
        app.timer.remaining_seconds = 1
        app._on_second_tick()
        await pilot.pause()

        assert app.timer.phase == TimerPhase.REST
        assert app.timer.completed_pomodoros == 1
        assert app.query_one("#cat-stage", CatStage).mode == StageMode.NAPPING
