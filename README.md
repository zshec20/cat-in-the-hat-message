# Line-by-line text prank

Sends a text file to someone one line at a time through the Messages app on a Mac.

## Setup

1. You need a Mac signed in to iMessage, with Python 3 (already on most Macs).
2. Save the script you want to send as `script.txt` in this folder, one message
   per line. Blank lines are skipped. The file is not included here because
   the movie script is copyrighted.

### Making script.txt from a saved web page

If you saved a transcript page from the web as an `.html` file, convert it:

```
python3 convert.py ~/Downloads/transcript.html
```

This strips the page's headers, tags and music-note junk and writes
`script.txt`, one message per line of dialogue. Add `--join` to send each
subtitle as a single message instead (about half as many, longer texts).

## Use

Preview first. This prints the lines and sends nothing:

```
python3 send_script.py --to "+15551234567" --dry-run
```

Send for real:

```
python3 send_script.py --to "+15551234567"
```

The first time, macOS asks whether Terminal may control Messages. Click OK.

## Group chats

If the group has a name (shown at the top of the chat), use it:

```
python3 send_script.py --group "Band Chat"
```

If the group has no name, list your chats and copy its id instead:

```
python3 send_script.py --list-groups
python3 send_script.py --group "iMessage;+;chat123456789"
```

The group must already exist in Messages, and everyone in it must be on
iMessage (blue bubbles). Groups with green-bubble members won't work.

## Options

| Option | What it does |
| --- | --- |
| `--to` | Phone number or iMessage email of one person |
| `--group` | Group chat name or id, instead of `--to` |
| `--list-groups` | Show your chats' names and ids, then exit |
| `--file` | Text file to send (default `script.txt`) |
| `--delay` | Seconds between messages (default `1.5`) |
| `--start` | Line number to start from, for resuming after a stop |
| `--limit` | Send only this many lines |
| `--dry-run` | Print the lines instead of sending |
| `--yes` | Skip the "type send" confirmation |

Press Ctrl+C to stop. The script prints the `--start` number to resume from.

## Notes

- It sends over iMessage, so the recipient needs an iPhone or other Apple device.
- Try `--file sample.txt --limit 3` on yourself before sending the full thing.
- A full movie script is over a thousand messages. Send it to someone who will
  find it funny.
