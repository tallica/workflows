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

### Added

- Reusable workflows `check.yml`, `pr.yml`, `go.yml` and `govulncheck.yml`,
  called as `tallica/workflows/.github/workflows/<name>@v1`.

[Unreleased]: https://github.com/tallica/workflows/commits/master
