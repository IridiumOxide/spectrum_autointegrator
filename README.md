# IntSpect

A tool to simplify comparing integrals of spectra stored in CSV files in a given directory.

Usage:

```sh
python intspect-cli.py PATH START END [--euro] [-c S] [--zerobase]
```
* PATH can point to a single file or a directory.
    * If it's a directory, all files inside will be processed as CSVs.
* START and END are floats determining the intervals over which the integrals will be computed
* Use `--euro` or `-e` if numbers are written with a `,` decimal separator instead of `.`
* Use `--csv_separator S` or `-c S` to set the expected csv delimiter to `S` (`;` by default)
* Use `--zerobase` to disable subtracting baseline

Have fun