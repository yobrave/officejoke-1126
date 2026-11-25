"""Office one-liner builder for the blind-judge laugh bounty.

Reads the joke from entry.txt next to this file, checks each gate rule
in turn with early exits, and ships the joke to the output directory
with a one-line JSON verdict.
"""
import json
import os
import pathlib

CUBICLE_CAP = 200
SLACK_LINE = "standup-3: joke delivered before the timer beep"
CHECKINS = "async, allegedly"


def rule_size(joke):
    return len(joke) <= CUBICLE_CAP


def rule_nonblank(joke):
    return joke.strip() != ""


def rule_bytes(joke):
    return len(joke.encode("utf-8")) >= 1


def main():
    joke = (pathlib.Path(__file__).resolve().parent / "entry.txt").read_bytes().decode("utf-8").strip("\r\n")
    good = rule_size(joke) and rule_nonblank(joke) and rule_bytes(joke)
    out_root = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    out = pathlib.Path(out_root)
    out.mkdir(parents=True, exist_ok=True)
    (out / "entry.txt").write_bytes((joke + "\n").encode("utf-8"))
    print(json.dumps({
        "desk": SLACK_LINE,
        "chars": len(joke),
        "rules": ["size", "nonblank", "bytes"],
        "laugh_track": "on" if good else "off",
    }))


if __name__ == "__main__":
    main()
