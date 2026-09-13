# Compatibility — Nancora Python Library

Nancora is designed to be lightweight, cross-platform, and fully compatible with modern scientific Python environments.

## Python Version Support

| Python Version | Status |
| :--- | :--- |
| **Python 3.10** | Supported & Tested |
| **Python 3.11** | Supported & Tested |
| **Python 3.12** | Supported & Tested (Default release target) |

## Key Dependencies

Nancora integrates cleanly with standard computational libraries:

| Package | Version Requirement | Purpose |
| :--- | :--- | :--- |
| **pandas** | `>= 2.0` | Data structure profiling & data manipulation |
| **numpy** | `>= 1.24` | Numerical statistical array calculations |
| **scipy** | `>= 1.10` | Statistical distributions & correlation metrics |
| **matplotlib** | `>= 3.7` | Static figure specification rendering |
| **plotly** | `>= 5.18` | Interactive plot specification helpers |
| **jinja2** | `>= 3.1` | Static HTML report template generation |
| **typer** | `>= 0.12` | Terminal Command-Line Interface (CLI) |

## Optional Extras

- **openpyxl** (`>= 3.1`): Enables Excel (`.xlsx`) reading via `nc.read_excel()` or CLI.
- **pyarrow** (`>= 14.0`): Enables Parquet (`.parquet`) reading via `nc.read_parquet()` or CLI.
