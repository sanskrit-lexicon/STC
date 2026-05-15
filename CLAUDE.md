# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**STC** is the corrections and research repository for the Cologne digitization of Stchoupak's *Dictionnaire Sanscrit-Français* (1932). The canonical source lives in `csl-orig/v02/stc/stc.txt`.

## Architecture

| Directory | Purpose |
|---|---|
| `verbs01/` | Root identification: maps STC verb entries to MW root spellings, identifies prefixed verbs |

### Verb root pipeline (`verbs01/`)

Identifies Stchoupak verb entries and maps them to MW equivalents with preverb resolution. See [STC issue #1](https://github.com/sanskrit-lexicon/STC/issues/1).

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/STC/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh stc ../../STCScan/2020
sh xmlchk_xampp.sh stc
```

## Dependencies

- **Python 3**
- **stc.txt** — in `$BASE/cologne/csl-orig/v02/stc/stc.txt`
