# workflows

For any agent (or person) working here. README.md says what the workflows do,
how to call them, how to test and how to release.

## Working on this

- **Committing and pushing are the maintainer's call.** Make the change, run the
  checks, say what happened and what couldn't be verified. Pushing, and above
  all moving the `v1` tag, each need an explicit go-ahead.
- **A workflow runs the calling repo's own Makefile and config.** Don't move
  what defines passing into this repo.
- **Compatibility is the contract.** Callers pin `@v1`, which moves with every
  1.x release. Anything a caller would have to change for is a new major
  version.
- **Every shared workflow is tested.** `self.yml` calls each one at the commit
  under test; `make test` fails when one isn't called there.
- **Shared workflows don't call each other.** `go.yml` repeats the govulncheck
  job instead; how `./` paths resolve in a nested call is not verified.
- **Every commit is ready to publish.** No secrets, personal data, home paths or
  real hosts; use placeholders.
- **Comments earn their line**, and README.md is the one home for usage: a fact
  in two places goes stale in one of them.

## Before committing

1. `make check` and `make fmt-check` pass.
2. Stage by path, never `git add -A` or `git add .`; commit only the index.
3. A change callers would notice has its CHANGELOG.md line in the same commit.
4. README.md still matches the workflows' jobs and inputs.

## Commits and branches

- [Conventional Commits](https://www.conventionalcommits.org/), checked by
  commitlint on pull requests; `feat!:` or `fix!:` for a breaking change.
- End with a trailer naming the agent that did the work, e.g.
  `Co-Authored-By: <agent/model> <noreply@example.com>`.
- `master` always works; small changes go on it directly.
