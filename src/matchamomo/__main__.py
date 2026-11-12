"""CLI entrypoint for MatchaMomo."""

from __future__ import annotations

import argparse
import sys

from matchamomo.app import MatchaMomoApp
from matchamomo.timer import (
    DEFAULT_FOCUS_MINUTES,
    DEFAULT_LONG_REST_INTERVAL,
    DEFAULT_LONG_REST_MINUTES,
    DEFAULT_REST_MINUTES,
    MAX_INTERVAL,
    MAX_MINUTES,
    MIN_INTERVAL,
    MIN_MINUTES,
)


def _bounded_int(min_val: int, max_val: int, label: str):
    def _parse(value: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"Expected integer {label}, got {value!r}") from exc
        if parsed < min_val or parsed > max_val:
            raise argparse.ArgumentTypeError(
                f"{label} must be between {min_val} and {max_val}, got {parsed}"
            )
        return parsed

    return _parse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="matchamomo",
        description="TUI Pomodoro timer animating a large orange cat and a small tortie.",
    )
    parser.add_argument(
        "-f",
        "--focus",
        type=_bounded_int(MIN_MINUTES, MAX_MINUTES, "minutes"),
        default=DEFAULT_FOCUS_MINUTES,
        help=f"Focus duration in minutes (default: {DEFAULT_FOCUS_MINUTES})",
    )
    parser.add_argument(
        "-r",
        "--rest",
        type=_bounded_int(MIN_MINUTES, MAX_MINUTES, "minutes"),
        default=DEFAULT_REST_MINUTES,
        help=f"Rest duration in minutes (default: {DEFAULT_REST_MINUTES})",
    )
    parser.add_argument(
        "-l",
        "--long-rest",
        type=_bounded_int(MIN_MINUTES, MAX_MINUTES, "minutes"),
        default=DEFAULT_LONG_REST_MINUTES,
        help=f"Long rest duration in minutes (default: {DEFAULT_LONG_REST_MINUTES})",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=_bounded_int(MIN_INTERVAL, MAX_INTERVAL, "pomodoros"),
        default=DEFAULT_LONG_REST_INTERVAL,
        help=f"Completed pomodoros before long rest (default: {DEFAULT_LONG_REST_INTERVAL})",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = MatchaMomoApp(
        focus_minutes=args.focus,
        rest_minutes=args.rest,
        long_rest_minutes=args.long_rest,
        long_rest_interval=args.interval,
    )
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
