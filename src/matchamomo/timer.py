"""Pomodoro timer state machine for MatchaMomo."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TimerPhase(StrEnum):
    """Phases of the Pomodoro timer."""

    IDLE = "idle"
    FOCUS = "focus"
    REST = "rest"
    LONG_REST = "long_rest"


class TimerEvent(StrEnum):
    """Events emitted when timer ticks cause a phase transition."""

    NONE = "none"
    STARTED_REST = "started_rest"
    STARTED_LONG_REST = "started_long_rest"
    COMPLETED_REST = "completed_rest"


DEFAULT_FOCUS_MINUTES = 25
DEFAULT_REST_MINUTES = 5
DEFAULT_LONG_REST_MINUTES = 15
DEFAULT_LONG_REST_INTERVAL = 4
MIN_MINUTES = 1
MAX_MINUTES = 180
MIN_INTERVAL = 1
MAX_INTERVAL = 20


@dataclass
class PomodoroTimer:
    """Configurable Pomodoro timer state machine.

    - Starts in ``IDLE`` with ``remaining_seconds = focus_minutes * 60``.
    - Starting transitions to ``FOCUS`` (cats chase each other).
    - When focus reaches 0, increments ``completed_pomodoros`` and transitions to
      ``LONG_REST`` every ``long_rest_interval`` pomodoros, otherwise ``REST``.
    - When rest or long rest reaches 0, transitions back to ``IDLE``.
    """

    focus_minutes: int = DEFAULT_FOCUS_MINUTES
    rest_minutes: int = DEFAULT_REST_MINUTES
    long_rest_minutes: int = DEFAULT_LONG_REST_MINUTES
    long_rest_interval: int = DEFAULT_LONG_REST_INTERVAL
    phase: TimerPhase = TimerPhase.IDLE
    running: bool = False
    remaining_seconds: int = 0
    completed_pomodoros: int = 0

    def __post_init__(self) -> None:
        self._validate_range(self.focus_minutes, "focus_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(self.rest_minutes, "rest_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(self.long_rest_minutes, "long_rest_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(
            self.long_rest_interval, "long_rest_interval", MIN_INTERVAL, MAX_INTERVAL
        )
        if self.remaining_seconds <= 0:
            self.remaining_seconds = self.focus_minutes * 60

    @staticmethod
    def _validate_range(value: int, name: str, min_val: int, max_val: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{name} must be an integer, got {value!r}")
        if value < min_val or value > max_val:
            raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")

    def configure(
        self,
        focus_minutes: int,
        rest_minutes: int,
        long_rest_minutes: int | None = None,
        long_rest_interval: int | None = None,
    ) -> None:
        """Update focus, rest, long rest durations (in minutes) and interval."""
        new_long_rest = self.long_rest_minutes if long_rest_minutes is None else long_rest_minutes
        new_interval = self.long_rest_interval if long_rest_interval is None else long_rest_interval
        self._validate_range(focus_minutes, "focus_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(rest_minutes, "rest_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(new_long_rest, "long_rest_minutes", MIN_MINUTES, MAX_MINUTES)
        self._validate_range(new_interval, "long_rest_interval", MIN_INTERVAL, MAX_INTERVAL)
        self.focus_minutes = focus_minutes
        self.rest_minutes = rest_minutes
        self.long_rest_minutes = new_long_rest
        self.long_rest_interval = new_interval
        if self.phase == TimerPhase.IDLE:
            self.remaining_seconds = self.focus_minutes * 60

    def start(self) -> None:
        """Start or resume the timer.

        If ``IDLE``, begins a ``FOCUS`` session.
        """
        if self.phase == TimerPhase.IDLE:
            self.phase = TimerPhase.FOCUS
            self.remaining_seconds = self.focus_minutes * 60
        self.running = True

    def pause(self) -> None:
        """Pause the active timer."""
        self.running = False

    def toggle(self) -> None:
        """Toggle between running and paused/idle."""
        if self.running:
            self.pause()
        else:
            self.start()

    def reset(self) -> None:
        """Reset back to IDLE state."""
        self.phase = TimerPhase.IDLE
        self.running = False
        self.remaining_seconds = self.focus_minutes * 60

    def skip_phase(self) -> TimerEvent:
        """Advance immediately to the next phase.

        - IDLE -> FOCUS (running)
        - FOCUS -> REST (running, cats nap)
        - REST -> IDLE (stopped, cats stand)
        """
        if self.phase == TimerPhase.IDLE:
            self.start()
            return TimerEvent.NONE
        if self.phase == TimerPhase.FOCUS:
            self.phase = TimerPhase.REST
            self.remaining_seconds = self.rest_minutes * 60
            self.running = True
            return TimerEvent.STARTED_REST
        self.reset()
        return TimerEvent.COMPLETED_REST

    def tick(self) -> TimerEvent:
        """Advance the timer by 1 second if running."""
        if not self.running or self.phase == TimerPhase.IDLE:
            return TimerEvent.NONE

        if self.remaining_seconds > 1:
            self.remaining_seconds -= 1
            return TimerEvent.NONE

        self.remaining_seconds = 0
        if self.phase == TimerPhase.FOCUS:
            self.completed_pomodoros += 1
            if self.completed_pomodoros % self.long_rest_interval == 0:
                self.phase = TimerPhase.LONG_REST
                self.remaining_seconds = self.long_rest_minutes * 60
                self.running = True
                return TimerEvent.STARTED_LONG_REST
            self.phase = TimerPhase.REST
            self.remaining_seconds = self.rest_minutes * 60
            self.running = True
            return TimerEvent.STARTED_REST

        if self.phase in (TimerPhase.REST, TimerPhase.LONG_REST):
            self.phase = TimerPhase.IDLE
            self.remaining_seconds = self.focus_minutes * 60
            self.running = False
            return TimerEvent.COMPLETED_REST

        return TimerEvent.NONE

    @property
    def total_phase_seconds(self) -> int:
        """Total duration in seconds of the current phase."""
        if self.phase == TimerPhase.REST:
            return self.rest_minutes * 60
        if self.phase == TimerPhase.LONG_REST:
            return self.long_rest_minutes * 60
        return self.focus_minutes * 60

    @property
    def formatted_time(self) -> str:
        """Return remaining time formatted as MM:SS."""
        minutes, seconds = divmod(max(0, self.remaining_seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"

    @property
    def progress(self) -> float:
        """Return completion ratio in [0.0, 1.0] for the current phase."""
        total = self.total_phase_seconds
        if total <= 0:
            return 0.0
        elapsed = total - self.remaining_seconds
        return max(0.0, min(1.0, elapsed / total))
