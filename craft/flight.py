"""What the hooks cannot predict, declared -- so a hook turn replays instead of being
re-argued.

A Stop hook's verdict is a pure function of outside things: the harness payload on
stdin, the session transcript, the record files the deciders read (claims.jsonl, filed
accounts, the seen-state), the filesystem layout that says which checkouts exist, and
the critic's model call. Each of those crosses HERE, as a named effect, and nowhere
else -- the smallest declaration that makes a verdict reproducible. The hook's own
source and account.schema.json are deliberately not effects: git already keeps them.

Writes are effects too, and that is load-bearing rather than thorough: the seen-state
a hook reads is the seen-state every session shares, and a replay that executed the
write would advance the live throttle while investigating it. Recording the write puts
it on the tape as testimony; replay serves it and touches nothing.

The tape carries transcript excerpts and command output, which is exactly what the
transcripts already carry, in the same directory tree, under the same user. The one
thing recorded here that the transcript does not hold is subprocess environments --
masked by name (`env`), because an environment block is where credentials live.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# One hook run parses the transcript up to four times (touched, silent_repos,
# reply_text, the corpus). Memoized OUTSIDE the effect so the tape holds the text
# once: the effect fires on the first ask and the memo answers the rest.
_transcripts: dict[str, str] = {}


def transcript_text(path) -> str:
    key = str(path)
    if key not in _transcripts:
        _transcripts[key] = read_transcript(key)
    return _transcripts[key]


def reset() -> None:
    """Forget the memoized transcripts. A replay in the same process must start with
    the memo empty, the way a fresh hook process does -- otherwise the memo answers
    where the tape holds an effect, and the feed reports an event nobody consumed."""
    _transcripts.clear()


def read_transcript(path: str) -> str:
    """Effect: the session transcript as this run saw it."""
    return Path(path).read_text(encoding="utf-8", errors="replace")


def file_text(path) -> str:
    """Effect: a record file the deciders read -- claims.jsonl, a filed account,
    the seen-state."""
    return Path(path).read_text(encoding="utf-8")


def write_text(path, text: str) -> None:
    """Effect: a record file the hook writes -- seen-state, residual.json, the
    critic's products. See the module docstring for why a write is recorded."""
    Path(path).write_text(text, encoding="utf-8")


def exists(path) -> bool:
    """Effect: whether the filesystem holds this path."""
    return Path(path).exists()


def is_dir(path) -> bool:
    """Effect: whether this path is a directory."""
    return Path(path).is_dir()


def listing(directory, pattern: str) -> list[str]:
    """Effect: the sorted matches of one glob, as strings."""
    return sorted(str(p) for p in Path(directory).glob(pattern))


def git_root(path) -> str | None:
    """Effect: the nearest enclosing git checkout, or None. One event per asked
    path, where recording the raw existence walk would be one per parent."""
    here = Path(str(path))
    for parent in [here, *here.parents]:
        if (parent / ".git").exists():
            return str(parent)
    return None


def working_dir() -> str:
    """Effect: where the harness launched the hook -- the repo the session sits in."""
    return os.getcwd()


def boundary(hook_name: str):
    from flight_recorder import Boundary

    me = sys.modules[__name__]
    return Boundary(
        effects=[(subprocess, ["run"]),
                 (me, ["read_transcript", "file_text", "write_text", "exists",
                       "is_dir", "listing", "git_root", "working_dir"])],
        redact={"env": None},
        header_extras={"hook": lambda: hook_name},
    )


def record(tools_module, hook_name: str) -> None:
    """One tape per hook turn, under this checkout's .craft/flight. On by default --
    a recorder that has to be remembered is off on the run that mattered;
    CRAFT_FLIGHT=0 opts out. Every failure is silent, because instrumentation that
    breaks the hook it instruments gets switched off, and then nothing is recorded
    at all."""
    if os.environ.get("CRAFT_FLIGHT", "1").strip().lower() in ("0", "off", "false", "no"):
        return
    try:
        from flight_recorder import install

        root = Path(__file__).resolve().parents[1]
        install(boundary(hook_name), tools_module,
                directory=str(root / ".craft" / "flight"))
    except Exception:
        pass
