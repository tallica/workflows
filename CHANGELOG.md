# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project
adheres to [Semantic Versioning](https://semver.org/). Commits follow
[Conventional Commits](https://www.conventionalcommits.org/): `feat` goes under
Added, `fix` under Fixed, a breaking `!` change is marked **Breaking**.

Entries are curated, not a dump of the git log: one line each, leading with what
the user sees or does differently, under 25 words. Internals and refactors don't
get an entry.

## [Unreleased]

## [1.1.1] - 2026-11-04

### Fixed

- `go.yml` no longer releases when a check job was cancelled (a timeout, say)
  while the run carried on; only skipped `format` is let through.

## [1.1.0] - 2026-11-04

### Added

- `pr.yml` lints with a default Conventional Commits config when the calling
  repo has no commitlint config; `commitlint: false` skips commitlint.
- `pr.yml` takes a `working-directory` for the commitlint job.

## [1.0.0] - 2026-11-04

### Added

- Reusable workflows `check.yml`, `pr.yml`, `go.yml` and `govulncheck.yml`,
  called as `tallica/workflows/.github/workflows/<name>@v1`.
- `format: false` on `check.yml` and `go.yml` skips the Prettier job, for repos
  without Prettier; a Go release still waits for every other job.

[Unreleased]: https://github.com/tallica/workflows/compare/v1.1.1...master
[1.1.1]: https://github.com/tallica/workflows/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/tallica/workflows/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/tallica/workflows/tree/v1.0.0
