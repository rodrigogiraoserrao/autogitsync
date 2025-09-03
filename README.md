# autogitsync

This CLI tool syncs your local changes to a git repository.
Useful when you're doing live-coding/teaching and want students to have near-live access to your work.

**How I use this**:

When teaching/giving tutorials at conferences, I create a repository for the workshop/course.
When the session starts, I start `autogitsync` and share the repository link with the audience.
Throughout the session, participants can go to the repository and they'll have the most recent version of my work and I don't have to keep adding, commiting, and pushing changes myself.

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
