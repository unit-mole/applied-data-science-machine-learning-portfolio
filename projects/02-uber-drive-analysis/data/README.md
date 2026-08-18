# Data Documentation — Uber Drive Behavior and Productivity Analysis

## Scope

1,155 source rows containing trip timestamps, categories, locations, distance, and purpose.

## Provenance and terms

The dataset is bundled in the original repository; upstream collection context and reuse terms are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `uber_drives.csv` | 87,647 | `c3f754ae34dc45294d932dc2ac6f0ee19b14432bbd303a2fb0e612a67aca9166` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
