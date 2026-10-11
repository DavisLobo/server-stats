# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- CPU usage analysis panel
- Disk usage analysis panel
- CLI arguments for configurable output path
- Optional Telegram / email report delivery
- Scheduled execution support (cron / systemd timer)
- Cross-platform support (macOS, WSL)

---

## [0.1.0] — 2026-10-11

### Added
- `src/main.py` entry point that orchestrates the full pipeline: memory check → user check → report generation, with structured `logging` output at each step.
- `src/analysis/server_memory.py` `check_memory()` function using `free -t -m` subprocess call; returns a typed `Dict[str, Any]` with fields: `total_mb`, `used_mb`, `free_mb`, `shared_mb`, `buff_cache_mb`, `available_mb`, derived `*_gb` float fields, `used_pct`, `free_pct`, and a human-readable `summary` string.
- `src/analysis/server_users.py` `check_users()` function using `w` subprocess call; parses the header line for uptime and load average via regex, column-aligns session rows from the output, and returns `total_users`, `uptime`, `load_average`, `headers`, `sessions`, and a `summary` string.
- `src/analysis/__init__.py` re-exports `check_memory` and `check_users` from the package root.
- **`src/report/server_report.py` `generate_report()` function producing a dark-themed `server_report.png` (Dracula palette) via `matplotlib`. Includes:
  - `_parse_memory_data()` helper accepting both `dict` and raw string inputs.
  - `_parse_users_data()` helper accepting both `dict` and raw string inputs.
  - Left panel: donut chart for RAM allocation (Used / Buffer+Cache / Free) with total GB label at center.
  - Right panel: KPI cards for Active Users, Uptime, and Load Average; session table (USER, TTY, FROM, LOGIN@, IDLE) when sessions are present, otherwise a friendly "no active sessions" notice.
  - Configurable `output_path` (default `server_report.png`) and optional `show` flag for interactive display.
- `src/report/__init__.py` re-exports `generate_report` from the package root.
- `LICENSE` MIT license (copyright 2026 Davi S.).
- `.gitignore` comprehensive Python `.gitignore` (covers `__pycache__`, virtual environments, build artifacts, IDE settings, and common framework directories).
- `README.md` and `CHANGELOG.md` project documentation files.

