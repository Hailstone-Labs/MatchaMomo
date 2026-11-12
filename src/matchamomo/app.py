"""Textual TUI application for MatchaMomo Pomodoro timer."""

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, ProgressBar, Static

from matchamomo.stage import CatStage, StageMode
from matchamomo.timer import (
    DEFAULT_FOCUS_MINUTES,
    DEFAULT_LONG_REST_INTERVAL,
    DEFAULT_LONG_REST_MINUTES,
    DEFAULT_REST_MINUTES,
    MAX_INTERVAL,
    MAX_MINUTES,
    MIN_INTERVAL,
    MIN_MINUTES,
    PomodoroTimer,
    TimerEvent,
    TimerPhase,
)


class ConfigScreen(ModalScreen[tuple[int, int, int, int] | None]):
    """Modal dialog to configure focus, rest, long rest durations and interval."""

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self,
        focus_minutes: int,
        rest_minutes: int,
        long_rest_minutes: int,
        long_rest_interval: int,
    ) -> None:
        super().__init__()
        self._focus_minutes = focus_minutes
        self._rest_minutes = rest_minutes
        self._long_rest_minutes = long_rest_minutes
        self._long_rest_interval = long_rest_interval

    def compose(self) -> ComposeResult:
        with Vertical(id="config-dialog"):
            yield Label("Timer Settings", id="config-title")
            yield Label("Focus duration (1-180 min):", classes="config-label")
            yield Input(
                value=str(self._focus_minutes),
                placeholder="25",
                id="focus-input",
                type="integer",
            )
            yield Label("Rest duration (1-180 min):", classes="config-label")
            yield Input(
                value=str(self._rest_minutes),
                placeholder="5",
                id="rest-input",
                type="integer",
            )
            yield Label("Long rest duration (1-180 min):", classes="config-label")
            yield Input(
                value=str(self._long_rest_minutes),
                placeholder="15",
                id="long-rest-input",
                type="integer",
            )
            yield Label("Pomodoros until long rest (1-20):", classes="config-label")
            yield Input(
                value=str(self._long_rest_interval),
                placeholder="4",
                id="interval-input",
                type="integer",
            )
            yield Static("", id="config-error")
            with Horizontal(id="config-buttons"):
                yield Button("Save", variant="primary", id="save-config")
                yield Button("Cancel", variant="default", id="cancel-config")

    def on_mount(self) -> None:
        self.query_one("#focus-input", Input).focus()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel-config":
            self.dismiss(None)
            return
        if event.button.id == "save-config":
            self._try_save()

    def on_input_submitted(self, _event: Input.Submitted) -> None:
        self._try_save()

    def _try_save(self) -> None:
        focus_raw = self.query_one("#focus-input", Input).value.strip()
        rest_raw = self.query_one("#rest-input", Input).value.strip()
        long_rest_raw = self.query_one("#long-rest-input", Input).value.strip()
        interval_raw = self.query_one("#interval-input", Input).value.strip()
        error_widget = self.query_one("#config-error", Static)
        try:
            focus_val = int(focus_raw)
            rest_val = int(rest_raw)
            long_rest_val = int(long_rest_raw)
            interval_val = int(interval_raw)
            if not (MIN_MINUTES <= focus_val <= MAX_MINUTES):
                raise ValueError(f"Focus must be {MIN_MINUTES}-{MAX_MINUTES} min.")
            if not (MIN_MINUTES <= rest_val <= MAX_MINUTES):
                raise ValueError(f"Rest must be {MIN_MINUTES}-{MAX_MINUTES} min.")
            if not (MIN_MINUTES <= long_rest_val <= MAX_MINUTES):
                raise ValueError(f"Long rest must be {MIN_MINUTES}-{MAX_MINUTES} min.")
            if not (MIN_INTERVAL <= interval_val <= MAX_INTERVAL):
                raise ValueError(f"Interval must be {MIN_INTERVAL}-{MAX_INTERVAL} pomodoros.")
        except ValueError as exc:
            error_widget.update(f"Invalid value: {exc}")
            return
        self.dismiss((focus_val, rest_val, long_rest_val, interval_val))


class MatchaMomoApp(App[None]):
    """TUI Pomodoro timer with two animated ASCII cats."""

    TITLE = "MatchaMomo"
    SUB_TITLE = "Cat Pomodoro Timer"

    CSS = """
    Screen {
        align: center middle;
        background: #1C1917;
        color: #FAFAF9;
    }

    #main-container {
        width: 100%;
        max-width: 90;
        height: auto;
        padding: 1 2;
        border: round #44403C;
        background: #292524;
    }

    #status-bar {
        width: 100%;
        height: 1;
        content-align: center middle;
        margin-bottom: 1;
    }

    #phase-label {
        width: 1fr;
        text-style: bold;
        color: #FDBA74;
    }

    #pomodoro-count {
        width: auto;
        color: #FCD34D;
        text-style: bold;
    }

    CatStage {
        width: 100%;
        height: 11;
        margin: 0 0 1 0;
        content-align: center middle;
    }

    #timer-readout {
        width: 100%;
        text-align: center;
        text-style: bold;
        color: #FAFAF9;
        margin-bottom: 1;
    }

    #progress-wrap {
        width: 100%;
        height: 1;
        align: center middle;
        margin-bottom: 1;
    }

    ProgressBar {
        width: 50;
    }

    #duration-summary {
        width: 100%;
        text-align: center;
        color: #A8A29E;
        margin-bottom: 1;
    }

    #controls {
        width: 100%;
        height: auto;
        align: center middle;
    }

    #controls Button {
        margin: 0 1;
    }

    ConfigScreen {
        align: center middle;
    }

    #config-dialog {
        width: 48;
        height: auto;
        max-height: 95%;
        padding: 0 2;
        border: round #FB923C;
        background: #292524;
    }

    #config-title {
        text-style: bold;
        color: #FDBA74;
        margin-bottom: 0;
    }

    .config-label {
        margin-top: 0;
        color: #D6D3D1;
    }

    #config-error {
        color: #F87171;
        height: 1;
        margin-top: 0;
    }

    #config-buttons {
        margin-top: 0;
        align: right middle;
        height: auto;
    }

    #config-buttons Button {
        margin-left: 1;
    }
    """

    BINDINGS = [
        Binding("space", "toggle_timer", "Start/Pause"),
        Binding("s", "toggle_timer", "Start/Pause", show=False),
        Binding("n", "skip_phase", "Next Phase"),
        Binding("r", "reset_timer", "Reset"),
        Binding("c", "open_config", "Configure"),
        Binding("plus", "inc_focus", "Focus +1m", show=False),
        Binding("equal", "inc_focus", "Focus +1m", show=False),
        Binding("minus", "dec_focus", "Focus -1m", show=False),
        Binding("right_square_bracket", "inc_rest", "Rest +1m", show=False),
        Binding("left_square_bracket", "dec_rest", "Rest -1m", show=False),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        focus_minutes: int = DEFAULT_FOCUS_MINUTES,
        rest_minutes: int = DEFAULT_REST_MINUTES,
        long_rest_minutes: int = DEFAULT_LONG_REST_MINUTES,
        long_rest_interval: int = DEFAULT_LONG_REST_INTERVAL,
    ) -> None:
        super().__init__()
        self.timer = PomodoroTimer(
            focus_minutes=focus_minutes,
            rest_minutes=rest_minutes,
            long_rest_minutes=long_rest_minutes,
            long_rest_interval=long_rest_interval,
        )

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="main-container"):
            with Horizontal(id="status-bar"):
                yield Static("", id="phase-label")
                yield Static("", id="pomodoro-count")
            yield CatStage(id="cat-stage")
            yield Static("", id="timer-readout")
            with Center(id="progress-wrap"):
                yield ProgressBar(
                    total=100, show_eta=False, show_percentage=False, id="progress-bar"
                )
            yield Static("", id="duration-summary")
            with Horizontal(id="controls"):
                yield Button("Start", variant="success", id="btn-toggle")
                yield Button("Rest Now", variant="warning", id="btn-skip")
                yield Button("Reset", variant="default", id="btn-reset")
                yield Button("Configure", variant="primary", id="btn-config")
        yield Footer()

    def on_mount(self) -> None:
        self.set_interval(1.0, self._on_second_tick)
        self._sync_ui()

    def _on_second_tick(self) -> None:
        if not self.timer.running:
            return
        event = self.timer.tick()
        if event in (
            TimerEvent.STARTED_REST,
            TimerEvent.STARTED_LONG_REST,
            TimerEvent.COMPLETED_REST,
        ):
            self.bell()
        self._sync_ui()

    def _desired_stage_mode(self) -> StageMode:
        if self.timer.phase == TimerPhase.LONG_REST:
            return StageMode.LONG_BREAK
        if self.timer.phase == TimerPhase.REST:
            return StageMode.NAPPING
        if self.timer.phase == TimerPhase.FOCUS and self.timer.running:
            return StageMode.CHASING
        return StageMode.STANDING

    def _sync_ui(self) -> None:
        stage = self.query_one("#cat-stage", CatStage)
        stage.mode = self._desired_stage_mode()

        phase_label = self.query_one("#phase-label", Static)
        if self.timer.phase == TimerPhase.IDLE:
            phase_label.update("READY — Cats standing together")
        elif self.timer.phase == TimerPhase.FOCUS:
            if self.timer.running:
                phase_label.update("FOCUS — Cats chasing each other!")
            else:
                phase_label.update("PAUSED — Catching their breath")
        elif self.timer.phase == TimerPhase.REST:
            if self.timer.running:
                phase_label.update("REST — Both cats are napping... zZz")
            else:
                phase_label.update("REST (PAUSED) — Both cats are napping... zZz")
        elif self.timer.phase == TimerPhase.LONG_REST:
            if self.timer.running:
                phase_label.update("LONG REST — Snack time & string play!")
            else:
                phase_label.update("LONG REST (PAUSED) — Snack time & string play!")

        count_label = self.query_one("#pomodoro-count", Static)
        count_label.update(
            f"Completed: {self.timer.completed_pomodoros} "
            f"(Long every {self.timer.long_rest_interval})"
        )

        readout = self.query_one("#timer-readout", Static)
        readout.update(f"[ {self.timer.formatted_time} ]")

        bar = self.query_one("#progress-bar", ProgressBar)
        bar.update(progress=int(self.timer.progress * 100))

        summary = self.query_one("#duration-summary", Static)
        summary.update(
            f"Focus: {self.timer.focus_minutes}m  |  Rest: {self.timer.rest_minutes}m  |  "
            f"Long Rest: {self.timer.long_rest_minutes}m (every {self.timer.long_rest_interval})"
        )

        toggle_btn = self.query_one("#btn-toggle", Button)
        if self.timer.running:
            toggle_btn.label = "Pause"
            toggle_btn.variant = "warning"
        elif self.timer.phase == TimerPhase.IDLE:
            toggle_btn.label = "Start"
            toggle_btn.variant = "success"
        else:
            toggle_btn.label = "Resume"
            toggle_btn.variant = "success"

        skip_btn = self.query_one("#btn-skip", Button)
        if self.timer.phase == TimerPhase.FOCUS:
            skip_btn.label = "Stop to Rest"
        elif self.timer.phase == TimerPhase.REST:
            skip_btn.label = "Finish Rest"
        elif self.timer.phase == TimerPhase.LONG_REST:
            skip_btn.label = "Finish Long Rest"
        else:
            skip_btn.label = "Start Focus"

    def action_toggle_timer(self) -> None:
        self.timer.toggle()
        self._sync_ui()

    def action_skip_phase(self) -> None:
        self.timer.skip_phase()
        self._sync_ui()

    def action_reset_timer(self) -> None:
        self.timer.reset()
        self._sync_ui()

    def action_open_config(self) -> None:
        def _apply_config(result: tuple[int, int, int, int] | None) -> None:
            if result is not None:
                focus_min, rest_min, long_rest_min, interval = result
                self.timer.configure(focus_min, rest_min, long_rest_min, interval)
                self._sync_ui()

        self.push_screen(
            ConfigScreen(
                self.timer.focus_minutes,
                self.timer.rest_minutes,
                self.timer.long_rest_minutes,
                self.timer.long_rest_interval,
            ),
            _apply_config,
        )

    def action_inc_focus(self) -> None:
        new_val = min(MAX_MINUTES, self.timer.focus_minutes + 1)
        self.timer.configure(new_val, self.timer.rest_minutes)
        self._sync_ui()

    def action_dec_focus(self) -> None:
        new_val = max(MIN_MINUTES, self.timer.focus_minutes - 1)
        self.timer.configure(new_val, self.timer.rest_minutes)
        self._sync_ui()

    def action_inc_rest(self) -> None:
        new_val = min(MAX_MINUTES, self.timer.rest_minutes + 1)
        self.timer.configure(self.timer.focus_minutes, new_val)
        self._sync_ui()

    def action_dec_rest(self) -> None:
        new_val = max(MIN_MINUTES, self.timer.rest_minutes - 1)
        self.timer.configure(self.timer.focus_minutes, new_val)
        self._sync_ui()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "btn-toggle":
            self.action_toggle_timer()
        elif btn_id == "btn-skip":
            self.action_skip_phase()
        elif btn_id == "btn-reset":
            self.action_reset_timer()
        elif btn_id == "btn-config":
            self.action_open_config()
