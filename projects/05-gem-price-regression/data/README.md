# Data Documentation — Cubic Zirconia Price Modeling

## Scope

26,967 cubic-zirconia records with physical measurements, quality grades, and price.

## Provenance and terms

Bundled in the original repository; market period, price units, sampling context, and redistribution terms are not fully documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `cubic_zirconia.csv` | 1,399,151 | `05066fa8c4a523990aa1d0a4e44e46ae7250bb088c982710db9c28fba2a2e6e7` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
