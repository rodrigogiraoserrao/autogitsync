# autogitsync

```
Usage: autogitsync [OPTIONS] REPO_PATH

  Automatically sync outgoing local changes into a git repository.

Options:
  --interval SECONDS   How often (in seconds) to attempt syncing.  [default:
                       60; x>=1]
  --verbose / --quiet  Turn logging on/off.  [default: verbose]
  --amend              Amend first sync commit with subsequent changes.
  -m, --message MSG    Commit message to use.  [default: Auto sync commit]
  -h, --help           Show this message and exit.
```
