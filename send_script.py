#!/usr/bin/env python3
"""Send a text file to someone line by line through the macOS Messages app.

Example:
    python3 send_script.py --to "+15551234567" --file script.txt --dry-run
    python3 send_script.py --to "+15551234567" --file script.txt
"""

import argparse
import platform
import subprocess
import sys
import time

# AppleScript that sends one message. The recipient and the text are passed in
# as arguments, so quotes or odd characters in a line can't break the script.
APPLESCRIPT = """
on run {targetHandle, messageText}
    tell application "Messages"
        set targetService to 1st account whose service type = iMessage
        set targetBuddy to participant targetHandle of targetService
        send messageText to targetBuddy
    end tell
end run
"""


def load_lines(path):
    """Read the file and return its non-empty lines, with whitespace trimmed."""
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def send_message(recipient, text):
    """Send one message through Messages. Raises an error if Messages refuses."""
    subprocess.run(
        ["osascript", "-e", APPLESCRIPT, recipient, text],
        check=True,
        capture_output=True,
        text=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Send a text file line by line through the macOS Messages app."
    )
    parser.add_argument("--to", required=True,
                        help="Phone number (like +15551234567) or iMessage email")
    parser.add_argument("--file", default="script.txt",
                        help="Text file to send (default: script.txt)")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Seconds to wait between messages (default: 1.5)")
    parser.add_argument("--start", type=int, default=1,
                        help="Line number to start from, for resuming (default: 1)")
    parser.add_argument("--limit", type=int,
                        help="Send at most this many lines")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the lines instead of sending them")
    parser.add_argument("--yes", action="store_true",
                        help="Skip the confirmation question")
    args = parser.parse_args()

    try:
        lines = load_lines(args.file)
    except FileNotFoundError:
        sys.exit(f"Can't find '{args.file}'. Put your text file next to this "
                 "script, or point to it with --file.")

    if args.start < 1 or args.start > len(lines):
        sys.exit(f"--start must be between 1 and {len(lines)} for this file.")

    first = args.start - 1
    last = len(lines) if args.limit is None else min(len(lines), first + args.limit)
    to_send = lines[first:last]
    total = len(lines)

    if not args.dry_run:
        if platform.system() != "Darwin":
            sys.exit("Sending only works on a Mac, because it uses the Messages "
                     "app. Use --dry-run to preview on other systems.")
        if not args.yes:
            minutes = len(to_send) * args.delay / 60
            print(f"About to send {len(to_send)} messages to {args.to} "
                  f"(roughly {minutes:.0f} min). Ctrl+C stops it at any time.")
            if input("Type 'send' to go: ").strip().lower() != "send":
                sys.exit("Cancelled. Nothing was sent.")

    number = args.start
    try:
        for number, line in enumerate(to_send, start=args.start):
            if args.dry_run:
                print(f"[{number}/{total}] {line}")
                continue
            send_message(args.to, line)
            print(f"[{number}/{total}] sent: {line}")
            if number < last:
                time.sleep(args.delay)
    except KeyboardInterrupt:
        sys.exit(f"\nStopped. To pick up where you left off, add: --start {number}")
    except subprocess.CalledProcessError as error:
        sys.exit(f"\nMessages refused line {number}: {error.stderr.strip()}\n"
                 f"Fix the problem, then resume with: --start {number}")

    print("Dry run finished. Nothing was sent." if args.dry_run else "All done.")


if __name__ == "__main__":
    main()
