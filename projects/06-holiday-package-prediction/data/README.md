# Data Documentation — Holiday Package Purchase Propensity

## Scope

872 records with purchase outcome, salary, age, education, children, and foreign-status fields.

## Provenance and terms

Bundled in the original repository; collection population, time period, and reuse terms are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `holiday_package.csv` | 23,701 | `288f6420d7d2fbfa733a9ac2a693a8edfb7be5a0c54391febb6a49646c950557` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
