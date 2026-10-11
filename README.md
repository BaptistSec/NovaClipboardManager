# Nova Clipboard Manager

A Windows clipboard manager written in Python. It keeps a history of clipboard items and shows them in a small window, so you can copy an older item back to the clipboard.

## Run it

You need Python and pywin32:

```sh
pip install pywin32
python NovaClipboardManager.py
```

A window opens with your clipboard history. Select an item and choose Copy to put it back on the clipboard. New clipboard items are saved to `clipboard_history.pkl` in the folder where you run the program. Choose Clear History to clear the saved list.

## Notes

- Windows only: it uses the win32clipboard API.
- Clipboard history is stored locally, without encryption. Avoid copying passwords, sign-in codes or other secrets while it is running.
- Do not open a clipboard history file from someone else: the program loads it using Python pickle.
- Not every clipboard format is supported or tested. This is an older project, not a guarantee of complete clipboard capture.
