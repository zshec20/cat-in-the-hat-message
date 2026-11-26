# Line-by-line text prank

Sends a text file to someone one line at a time through the Messages app on a Mac.

## Setup

1. You need a Mac signed in to iMessage, with Python 3 (already on most Macs).
2. Save the script you want to send as `script.txt` in this folder, one line of
   dialogue per line. Blank lines are skipped. The file is not included here
   because the movie script is copyrighted.

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

## Options

| Option | What it does |
| --- | --- |
| `--to` | Phone number or iMessage email of the recipient (required) |
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
