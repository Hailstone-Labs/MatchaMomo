# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-12

### Added
- TUI Pomodoro timer built with Textual and managed by `uv`.
- Animated ASCII art sprites for a large orange cat and a small tortie cat:
  - Standing next to each other when idle (`IDLE`).
  - Chasing each other across the stage during focus sessions (`FOCUS`).
  - Napping together during short rest breaks (`REST`).
  - Orange cat eating a snack while the tortie plays with a string during long rest breaks (`LONG_REST`).
- Configurable focus, rest, long rest durations (in minutes) and long rest interval (in completed pomodoros) via CLI flags and the in-app settings modal.
- GitHub Actions CI, Release (GitHub Releases + PyPI Trusted Publishing), and Dependabot configuration.
