# Data Documentation — Wine Sales Forecasting with Rolling-Origin Validation

## Scope

187 monthly Rose and Sparkling observations from January 1980 through July 1995.

## Provenance and terms

Bundled in the original repository; commercial source, currency/units, and redistribution terms are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `rose.csv` | 2,323 | `e3553bd7f11fa3c804c89c74222e4649eca82112c819a88a9eb869a871d19198` |
| `sparkling.csv` | 2,639 | `539745fc03e143ea914d98d7dbd38f11bc51f6dab108e0a003e2f7295e3aa7b6` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
