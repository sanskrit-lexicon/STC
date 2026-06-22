# STC front matter — OCR + translations

Faithful OCR of the **front matter** (title page and *Avant-propos* / Foreword) of:

> N. Stchoupak, L. Nitti et L. Renou, **_Dictionnaire Sanskrit-Français_**. Paris: Librairie d'Amérique et d'Orient, Adrien Maisonneuve, 1932. — *Publications de l'Institut de Civilisation Indienne.*

Source scans are the Cologne csldoc preface pages:
<https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/stcpref.html>

**Source language: French.** The base `stcprefNN.md` files carry the verbatim French transcription; `.en.md` and `.ru.md` are faithful translations. Sanskrit work-titles and transliterated forms are kept verbatim in every language (the dictionary uses the older Lepsius-style romanisation: `ç` = ś, `ṛ ṣ ṇ ṭ ḍ ñ` with dots, etc.). The tiny Cologne digitizer running header/footer stamps are omitted as they are not part of the original.

## File conventions

| Suffix | Meaning |
|---|---|
| `stcprefNN.md` | French source transcription (page NN) |
| `stcprefNN.en.md` | English translation |
| `stcprefNN.ru.md` | Russian translation |
| `stcpref_all.<lang>.md` | All pages concatenated, with a table of contents |
| `build_combined.py` | Reproducible generator of the `*_all.*` files (`DICT=stc python build_combined.py`) |
| `scans/` | The original `.jpg` scan pages |

## Consolidated editions

| Edition | File |
|---|---|
| Français (source) | [stcpref_all.fr.md](stcpref_all.fr.md) |
| English | [stcpref_all.en.md](stcpref_all.en.md) |
| Русский | [stcpref_all.ru.md](stcpref_all.ru.md) |
| Build script | [build_combined.py](build_combined.py) |

## Contents

| NN | Section | Vol. | Source (FR) | English | Russian | Scan |
|---|---|---|---|---|---|---|
| 01 | Title Page | 1 | [fr](stcpref01.md) | [en](stcpref01.en.md) | [ru](stcpref01.ru.md) | [stchou-vor0001.jpg](scans/stchou-vor0001.jpg) |
| 02 | Avant-propos, 1 | 1 | [fr](stcpref02.md) | [en](stcpref02.en.md) | [ru](stcpref02.ru.md) | [stchou-vor0005.jpg](scans/stchou-vor0005.jpg) |
| 03 | Avant-propos, 2 (p. II) | 1 | [fr](stcpref03.md) | [en](stcpref03.en.md) | [ru](stcpref03.ru.md) | [stchou-vor0007.jpg](scans/stchou-vor0007.jpg) |
| 04 | Avant-propos, 3 — abbreviations (p. III) | 1 | [fr](stcpref04.md) | [en](stcpref04.en.md) | [ru](stcpref04.ru.md) | [stchou-vor0008.jpg](scans/stchou-vor0008.jpg) |
| 05 | Avant-propos, 4 (p. IV) | 1 | [fr](stcpref05.md) | [en](stcpref05.en.md) | [ru](stcpref05.ru.md) | [stchou-vor0009.jpg](scans/stchou-vor0009.jpg) |

## Notes

- The *Avant-propos* is unsigned and undated; it closes with thanks to the Académie des Inscriptions et Belles-Lettres and to M. A. Foucher, and homage to the late É. Senart, but carries no byline or place/date.
- Page 04 is a two-column list of the French grammatical abbreviations used throughout the dictionary; the keys are kept verbatim and the expansions translated.
- Footnotes are reproduced per page below a horizontal rule.
