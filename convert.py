#!/usr/bin/env python3
"""Turn a saved transcript web page (.html) into a clean script.txt.

Example:
    python3 convert.py ~/Downloads/transcript.html
    python3 convert.py ~/Downloads/transcript.html --join
"""

import argparse
import html
import re
import sys


def read_text(path):
    """Read the file, coping with older Windows-encoded web pages."""
    data = open(path, "rb").read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252", errors="ignore")


def clean_line(line):
    """Strip HTML tags, music-note junk and extra spaces from one line."""
    line = re.sub(r"<[^>]+>", "", line)        # remove tags like <i> and </p>
    line = html.unescape(line)                 # &nbsp; &amp; etc.
    line = re.sub(r"@+[^\w\s\[(\"']*", " ", line)  # "@" stands in for music notes
    return re.sub(r"\s+", " ", line).strip()


def convert(page, join):
    """Return the list of messages found in the page."""
    # Transcript sites keep the dialogue inside a <pre> block; the rest of the
    # page is headers and links we don't want.
    match = re.search(r"<pre[^>]*>(.*?)</pre>", page, re.S | re.I)
    body = match.group(1) if match else page

    messages = []
    # Each <p> block is one subtitle card, usually 1-3 short lines.
    for block in re.split(r"<p[^>]*>", body, flags=re.I):
        lines = [clean_line(raw) for raw in block.splitlines()]
        lines = [line for line in lines if line]
        if join and lines:
            messages.append(" ".join(lines))
        else:
            messages.extend(lines)
    return messages


def main():
    parser = argparse.ArgumentParser(
        description="Turn a saved transcript web page into script.txt.")
    parser.add_argument("page", help="The .html file you saved or downloaded")
    parser.add_argument("--out", default="script.txt",
                        help="File to write (default: script.txt)")
    parser.add_argument("--join", action="store_true",
                        help="Send each subtitle as one message instead of "
                             "one message per line (fewer, longer texts)")
    args = parser.parse_args()

    try:
        page = read_text(args.page)
    except FileNotFoundError:
        sys.exit(f"Can't find '{args.page}'.")

    messages = convert(page, args.join)
    if not messages:
        sys.exit("Found no text in that file.")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(messages) + "\n")
    print(f"Wrote {len(messages)} messages to {args.out}.")


if __name__ == "__main__":
    main()
