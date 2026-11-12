# MatchaMomo

A TUI-based Pomodoro timer built with [Textual](https://textual.textualize.io/) and managed with [`uv`](https://docs.astral.sh/uv/), featuring two animated ASCII cats: a large orange cat and a small tortie.

## Features

- **Animated ASCII Cats**
  - **Ready (`IDLE`)**: Both cats stand next to each other with subtle tail wags and blinks.
  - **Focus (`FOCUS`)**: When the timer starts, the cats chase each other back and forth across the stage.
  - **Rest (`REST`)**: When focus ends and rest begins, both cats curl up and nap (`zZz`).
  - **Long Rest (`LONG_REST`)**: After a configurable number of completed pomodoros, the large orange cat eats a snack while the small tortie plays with a string.
- **Configurable Durations (in minutes)**:
  - Focus duration (default: `25` min)
  - Rest duration (default: `5` min)
  - Long rest duration (default: `15` min)
  - Long rest interval (default: every `4` completed pomodoros)

## Getting Started

Requires Python `>=3.12` and `uv`.

```zsh
# Clone and sync dependencies
uv sync

# Run MatchaMomo with default settings
uv run matchamomo

# Or customize durations via CLI flags
uv run matchamomo --focus 25 --rest 5 --long-rest 15 --interval 4
```

### CLI Options

| Flag | Description | Default |
| --- | --- | --- |
| `-f`, `--focus` | Focus duration in minutes (`1–180`) | `25` |
| `-r`, `--rest` | Rest duration in minutes (`1–180`) | `5` |
| `-l`, `--long-rest` | Long rest duration in minutes (`1–180`) | `15` |
| `-i`, `--interval` | Completed pomodoros before long rest (`1–20`) | `4` |

### Keybindings

| Key | Action |
| --- | --- |
| `Space` / `s` | Start, pause, or resume timer |
| `n` | Skip to next phase (e.g., stop focus to rest) |
| `r` | Reset timer to idle |
| `c` | Open Timer Settings modal |
| `+` / `-` | Increase / decrease focus minutes by 1 |
| `]` / `[` | Increase / decrease rest minutes by 1 |
| `q` | Quit |

## Development

```zsh
# Run tests
uv run pytest -v

# Lint and format check
uv run ruff check .
uv run ruff format --check .

# Type check
uv run mypy src tests
```
