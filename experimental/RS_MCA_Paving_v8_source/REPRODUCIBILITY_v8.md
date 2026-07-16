# Reproducibility record for `RS_MCA_Paving_v8`

Date: 2026-07-16

## Contents and scope

- `RS_MCA_Paving_v8.tex` is the manuscript source.
- `RS_MCA_Paving_v8.pdf` is the compiled 53-page A4 manuscript.
- `verify_paving_mca_v8.py` checks the unconditional finite arithmetic used in the paving, circle, all-radius, field-budget, and retained BCHKS comparisons.
- `verify_retained_bchks_v8.py` checks only the arithmetic consequences of the parameter-retained factor-lift assumption. It does **not** prove that assumption.
- `AI_USE_v8.md` records the manuscript's AI-use disclosure in more detail.

The proof-development repository is pinned at
<https://github.com/przchojecki/rs-mca/tree/02728b208ea785d02115ea967236aebf653b31ec>.
The two verification scripts are ancillary files of this source release and are not claimed to occur in that snapshot.

## Arithmetic verification

Run with Python 3.12 or a compatible Python 3 interpreter:

```sh
python3 verify_paving_mca_v8.py
python3 verify_retained_bchks_v8.py
```

Expected output:

```text
v8 unconditional arithmetic: all checks passed
v8 conditional retained-lift arithmetic: all checks passed
NOTE: the Parameter-retained factor lift remains an assumption.
```

Both scripts passed under Python 3.12.13 on 2026-07-16.

## TeX build

On a standard TeX Live installation with `amsart`, compile with:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error RS_MCA_Paving_v8.tex
```

The checked build used pdfTeX 1.40.25 (TeX Live 2023) and produced 53 A4 pages. The final log contained no errors, unresolved references or citations, overfull or underfull boxes, or LaTeX warnings.

## SHA-256 digests

```text
dd936a52e3cac8f96d35c9e1b0c506654053cf64e1ea302acd83a971110be60a  RS_MCA_Paving_v8.tex
5a7bcc58e926a2f74c0b6014ad65247e9af1761ef5fdbcf3e08867f3637309c3  RS_MCA_Paving_v8.pdf
8193c388aeccd92bf7b610fa6747de67d91cab6b56621eabd91ed70e0884f8bf  verify_paving_mca_v8.py
af01479e58cfbf371fea211eacb6ff882fed8ac08967043158e88dd5a79a4da8  verify_retained_bchks_v8.py
58f8d772f7c61f723ff570425bf04499e4ca769180930e06375d487fdcb14e15  AI_USE_v8.md
```

These digests identify the individual release files. PDF bytes may change if the document is rebuilt because TeX records build timestamps; the mathematical content and pagination should remain unchanged.
