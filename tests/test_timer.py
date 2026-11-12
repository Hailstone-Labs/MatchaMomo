"""Unit tests for PomodoroTimer state machine."""

import pytest

from matchamomo.timer import PomodoroTimer, TimerEvent, TimerPhase


def test_initial_state() -> None:
    timer = PomodoroTimer(focus_minutes=25, rest_minutes=5)
    assert timer.phase == TimerPhase.IDLE
    assert timer.running is False
    assert timer.remaining_seconds == 25 * 60
    assert timer.formatted_time == "25:00"
    assert timer.completed_pomodoros == 0


def test_configure_minutes() -> None:
    timer = PomodoroTimer()
    timer.configure(focus_minutes=45, rest_minutes=15)
    assert timer.focus_minutes == 45
    assert timer.rest_minutes == 15
    assert timer.remaining_seconds == 45 * 60
    assert timer.formatted_time == "45:00"


@pytest.mark.parametrize("bad_value", [0, -5, 181, True, "25"])
def test_configure_validation(bad_value: object) -> None:
    timer = PomodoroTimer()
    with pytest.raises(ValueError):
        timer.configure(focus_minutes=bad_value, rest_minutes=5)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        timer.configure(focus_minutes=25, rest_minutes=bad_value)  # type: ignore[arg-type]


def test_focus_to_rest_to_idle_transition() -> None:
    timer = PomodoroTimer(focus_minutes=1, rest_minutes=1)
    timer.start()
    assert timer.phase == TimerPhase.FOCUS
    assert timer.running is True

    for _ in range(59):
        assert timer.tick() == TimerEvent.NONE
    assert timer.remaining_seconds == 1

    # 60th tick completes focus and starts rest
    assert timer.tick() == TimerEvent.STARTED_REST
    assert timer.phase == TimerPhase.REST
    assert timer.running is True
    assert timer.remaining_seconds == 60
    assert timer.completed_pomodoros == 1

    for _ in range(59):
        assert timer.tick() == TimerEvent.NONE
    assert timer.tick() == TimerEvent.COMPLETED_REST
    assert timer.phase == TimerPhase.IDLE
    assert timer.running is False
    assert timer.remaining_seconds == 60


def test_skip_and_reset() -> None:
    timer = PomodoroTimer(focus_minutes=10, rest_minutes=3)
    timer.start()
    assert timer.phase == TimerPhase.FOCUS

    event = timer.skip_phase()
    assert event == TimerEvent.STARTED_REST
    assert timer.phase == TimerPhase.REST
    assert timer.remaining_seconds == 3 * 60
    assert timer.running is True

    timer.reset()
    assert timer.phase == TimerPhase.IDLE
    assert timer.running is False
    assert timer.remaining_seconds == 10 * 60


def test_long_rest_after_configured_pomodoros() -> None:
    timer = PomodoroTimer(
        focus_minutes=1,
        rest_minutes=1,
        long_rest_minutes=12,
        long_rest_interval=2,
    )
    # 1st pomodoro -> regular rest
    timer.start()
    timer.remaining_seconds = 1
    assert timer.tick() == TimerEvent.STARTED_REST
    assert timer.completed_pomodoros == 1
    assert timer.phase == TimerPhase.REST
    assert timer.remaining_seconds == 60

    # Complete regular rest -> idle
    timer.remaining_seconds = 1
    assert timer.tick() == TimerEvent.COMPLETED_REST
    assert timer.phase == TimerPhase.IDLE

    # 2nd pomodoro -> long rest!
    timer.start()
    timer.remaining_seconds = 1
    assert timer.tick() == TimerEvent.STARTED_LONG_REST
    assert timer.completed_pomodoros == 2
    assert timer.phase == TimerPhase.LONG_REST
    assert timer.running is True
    assert timer.remaining_seconds == 12 * 60

    # Complete long rest -> idle
    timer.remaining_seconds = 1
    assert timer.tick() == TimerEvent.COMPLETED_REST
    assert timer.phase == TimerPhase.IDLE
    assert timer.running is False
