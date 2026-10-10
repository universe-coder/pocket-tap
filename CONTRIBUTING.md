# Contributing

Issues and pull requests are welcome. Bug reports are most useful with your OS, the phone and browser, and the PC program's console output.

## Development

```sh
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
python -m pc_remote --dry-run   # log commands instead of pressing keys
```

The phone app is plain HTML, CSS and JavaScript in `pc_remote/static/`, with no build step: edit and reload the page on the phone.

## Adding or fixing a translation

1. Copy `pc_remote/static/locales/en.json` to `<code>.json` (an [IETF language code](https://en.wikipedia.org/wiki/IETF_language_tag), e.g. `fr`) and translate the values. Keep `\n` line breaks and the arrows in place.
2. Add the language with its own name to `LANGUAGES` in `pc_remote/static/i18n.js`. For a right-to-left language, also add it to `RTL_LANGUAGES`.
3. Add the console messages to `MESSAGES` and the code to `LANGUAGES` in `pc_remote/i18n.py`.
4. Optionally translate the README into `docs/README.<code>.md` and link it from the language line at the top of every README.

`python -m pytest` checks that every language has every string.
