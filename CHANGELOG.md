# Changelog

## 4.0.1 — 2026-05-04

### Fixed
- Define an empty `dev` group in `[dependency-groups]` so `uv sync --group dev`
  runs in CI without `error: Group 'dev' is not defined in the project's
  'dependency-groups' table`.

### Changed
- Drop Python 3.12 from the CI matrix.

## 4.0.0 — 2026-05-04

### Changed
- **BREAKING** — Reduce package scope: drop the `doc/` Sphinx site in favour
  of a single `README.md`.
- **BREAKING** — Major cleanup of the bundled JavaScript; trim it to the
  features actually exercised by `{% show_more %}` (click + optional
  infinite scroll). jQuery and the legacy multi-page / on-screen-callbacks
  helpers are gone — the file is now a dependency-free vanilla module
  exposing `endlessPaginate()` and `EndlessPagination`.
- Migrate the project from Rye to uv.
- Numerous internal fixes shipped alongside the cleanup.

## 3.1.0 — 2026-05-04

### Added
- Support Django 6.0.

### Changed
- Rename and streamline the publish GitHub Action (no Python setup or cache
  needed for the publish step).

## 3.0.2 — 2024-08-19

### Fixed
- Install Rye in CI so the test workflow can resolve dependencies.
