# workflows

Reusable GitHub Actions workflows. Each calling repo keeps what defines passing
(its Makefile, its commitlint config if it has one, `scripts/release-notes.sh`);
these workflows only run them, so the CI wiring and action versions live in one
place.

## Workflows

| Workflow          | Jobs                                                                                           | Inputs (default)                                                                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `check.yml`       | `make check`; `make fmt-check`                                                                 | `node-version` (`24`), `format` (`true`)                                                                                                          |
| `pr.yml`          | commitlint on commits and title; CHANGELOG guard                                               | `commitlint` (`true`), `working-directory` (`.`), `node-version` (`24`), `commitlint-version` (`19.8.1`), `changelog-label` (`user-facing`)       |
| `go.yml`          | build, vet, race tests; golangci-lint; Prettier; govulncheck; notices; GoReleaser on `v*` tags | `working-directory` (`.`), `golangci-lint-version` (`v2.14.0`), `node-version` (`24`), `format` (`true`), `notices` (`false`), `release` (`true`) |
| `govulncheck.yml` | `make audit`, for a weekly schedule in the calling repo                                        | `working-directory` (`.`)                                                                                                                         |

What the calling repo needs: `make check` and `make fmt-check` for `check.yml`;
`go.mod`, `make fmt-check`, `make audit` and `scripts/release-notes.sh` for
`go.yml`. A repo without Prettier passes `format: false` and needs no
`make fmt-check`; `notices: true` also needs `make notices-check`.

`pr.yml` uses the repo's commitlint config when it has one (any file name
commitlint reads, or a `commitlint` key in `package.json`). Without one it uses
the default: `@commitlint/config-conventional`, no limit on body line length,
and Dependabot's `build(deps): Bump ...` subjects ignored. `commitlint: false`
skips commitlint and keeps only the CHANGELOG guard.

## Usage

Call a workflow from a job, pinned to the major version:

```yaml
# .github/workflows/pr.yml
name: PR
on:
  pull_request:
    types: [opened, edited, synchronize, reopened, labeled, unlabeled]
permissions:
  contents: read
jobs:
  pr:
    uses: tallica/workflows/.github/workflows/pr.yml@v1
```

`go.yml`'s release job needs `contents: write`. A called workflow can't raise
its permissions, so the calling job grants it:

```yaml
jobs:
  go:
    uses: tallica/workflows/.github/workflows/go.yml@v1
    permissions:
      contents: write
```

A `schedule:` trigger only runs in the repo that declares it, so a Go repo keeps
a small workflow with `on: schedule` that calls `govulncheck.yml`.

`@v1` follows the latest 1.x release, so a fix reaches every caller on its next
run. Anything a caller would have to change for (a renamed input, a new required
file, a removed job) is a new major version; Dependabot's `github-actions`
updates propose the move.

## Development

```sh
make check      # actionlint, and every shared workflow is called by self.yml
make fmt-check  # Prettier
```

`make lint` runs actionlint, built with `go run` when it isn't installed.
`make test` fails when a shared workflow isn't callable or isn't called by
`self.yml`. The real test is CI: `self.yml` calls every shared workflow at the
pushed commit, `go.yml` and `govulncheck.yml` against the Go module in
`testdata/go` (`make -C testdata/go check` and `make -C testdata/go audit` run
the same locally). A release job only shows itself in a calling repo's tagged
release; check the first one after changing it.

## Releasing

1. `git fetch -q`; `master` is clean, up to date and `make check` passes.
2. In CHANGELOG.md, rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`, add
   an empty `## [Unreleased]` above it, and update the compare links at the
   bottom.
3. Commit only CHANGELOG.md as `chore(release): vX.Y.Z`, then tag it
   `git tag -a vX.Y.Z -m vX.Y.Z` and move the major tag:
   `git tag -fa v1 -m v1 'vX.Y.Z^{}'` (the commit, not the `vX.Y.Z` tag object).
4. Push with `git push && git push origin vX.Y.Z && git push -f origin v1`.
   Pushing `v1` changes every caller's CI at once, so it waits for the
   maintainer's go-ahead.

## License

MIT, see [LICENSE](LICENSE).
