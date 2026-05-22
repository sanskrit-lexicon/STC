### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `stc.txt`.

I ran the same two-job recipe over `csl-orig/v02/stc/stc.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `stcissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `stc.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<ab> word </ab>` | `<ab>word</ab>` |
| `<F> word </F>` | `<F>word</F>` |
| `<lang> word </lang>` | `<lang>word</lang>` |

Whitespace trimming applies to all 3 paired tag(s) in `stc.txt`: `<ab>`, `<F>`, `<lang>`. The original file is never modified — output goes to `stc_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). **Output is byte-identical to source** (no auto-fixes triggered).

### Closing-tag inventory in current `stc.txt`

| Tag | Count |
|---|---:|
| `</ab>` | 80 |
| `</387)>` | ? |
| `</F>` | 8 |
| `</lang>` | 1 |

### What it found in current `stc.txt`

- 0 whitespace trims — byte-identical to source.
- 9,146 within-line adjacent `</ab> <ab>` pairs — the largest count of all dictionaries processed. Listed for verification.
- 19 within-line `<ab n="…">` non-standard expansion matches — French words ("parfait" ×6, "surtout" ×3, etc.).
- 20 `{{old → new || …}}` correction records present.

### Usage

```
cd stcissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/stc/stc.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `stc_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

French-Sanskrit dictionary; <ab> is the dominant paired tag.

### Severity

`minor`
