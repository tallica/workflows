#!/bin/sh
# Rewrite a markdown file's repo-relative links to absolute ones at a tag.
#
# Usage: scripts/absolute-links.sh v1.2.3 < README.md
#
# Away from a checkout - on a release page or in a release tarball -
# relative links have nothing to resolve against. Pinning them to the tag
# points each one at the tree that release shipped with.
set -eu

tag=${1:-}
if [ -z "$tag" ]; then
	echo "usage: $0 <tag>" >&2
	exit 2
fi

repo=https://github.com/example/fixture
raw=https://raw.githubusercontent.com/example/fixture

# An embedded image wants the file itself, not the page GitHub wraps it in.
sed -E \
	-e "s|!\[([^]]*)\]\(([A-Za-z0-9._/-][A-Za-z0-9._/-]*)\)|![\1](${raw}/${tag}/\2)|g" \
	-e "s|\]\(([A-Za-z0-9._/-][A-Za-z0-9._/#-]*)\)|](${repo}/blob/${tag}/\1)|g"
