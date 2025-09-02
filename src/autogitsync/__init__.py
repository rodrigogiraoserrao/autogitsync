#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Optional

import click
from git import Repo, GitCommandError, InvalidGitRepositoryError, NoSuchPathError  # type: ignore
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def _print(msg: str | Panel, *, quiet: bool, style: Optional[str] = None) -> None:
    if not quiet:
        console.print(msg, style=style)


def _find_remote(repo: Repo) -> Optional[str]:
    names = [r.name for r in repo.remotes]
    if not names:
        return None
    return "origin" if "origin" in names else names[0]


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--interval",
    type=click.IntRange(min=1),
    default=60,
    show_default=True,
    help="How often (in seconds) to attempt syncing.",
)
@click.option(
    "--quiet/--verbose",
    default=False,  # default is --verbose
    help="Turn logging off/on.",
)
@click.option(
    "--amend",
    is_flag=True,
    default=False,
    help="Amend first sync commit with subsequent changes.",
)
@click.option(
    "--message",
    "-m",
    default="Auto sync commit",
    show_default=True,
    metavar="MSG",
    help="Commit message to use.",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, exists=True, path_type=Path),
    default=Path("."),
    show_default=True,
    help="Directory to sync (a Git repository).",
)
def gitsync(interval: int, quiet: bool, amend: bool, message: str, path: Path) -> None:
    """Automatically sync a Git repository by add/commit/push in a loop."""
    try:
        repo_folder = path.resolve()
        os.chdir(repo_folder)
        repo = Repo(repo_folder)
    except InvalidGitRepositoryError:
        console.print(f"[red]Not a valid repo:[/red] {path}")
        sys.exit(1)
    except NoSuchPathError:
        console.print(f"[red]Not a valid path:[/red] {path}")
        sys.exit(1)

    start_msg = Text(f"gitsync starting at {repo_folder}", style="bold")
    _print(Panel(start_msg, title="GitSync", expand=False), quiet=quiet)

    remote_name = _find_remote(repo)
    if remote_name is None:
        console.print(
            "[red]Error:[/red] No Git remotes configured for this repository."
        )
        sys.exit(2)

    _print(
        f"Using remote [bold]{remote_name}[/bold]. Press Ctrl+C to stop.", quiet=quiet
    )

    first_commit = True
    while True:
        try:
            if not repo.is_dirty(untracked_files=True):
                _print("No new changes to sync.", quiet=quiet)
                continue

            repo.git.add(all=True)

            will_amend = amend and not first_commit
            if will_amend:
                # Try to amend, fall back to regular commit if it fails.
                try:
                    repo.git.commit("--amend", "-m", message)
                except GitCommandError:
                    repo.index.commit(message)
                    will_amend = False
            else:
                repo.index.commit(message)
                first_commit = False

            push_info_list = repo.remote(remote_name).push(
                force=amend and not first_commit
            )
            push_info_list.raise_if_error()

            _print(
                ("Pushed changes. (amended)" if will_amend else "Pushed changes."),
                quiet=quiet,
                style="green",
            )

        except KeyboardInterrupt:
            _print("\nStopping gitsync. Bye!", quiet=False)
            break
        except Exception as e:
            _print(f"Sync failed: {e!s}", quiet=quiet, style="red")
            sys.exit(3)

        time.sleep(interval)


if __name__ == "__main__":
    gitsync()
