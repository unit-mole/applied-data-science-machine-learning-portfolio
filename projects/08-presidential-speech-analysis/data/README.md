# Data Documentation — U.S. Presidential Inaugural Speech Analysis

## Scope

The 1941 Roosevelt, 1961 Kennedy, and 1973 Nixon inaugural addresses stored as three workbooks.

## Provenance and terms

The original project identifies NLTK's inaugural corpus as the source; local workbooks preserve imported snapshots.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `kennedy_1961.xlsx` | 12,501 | `9798609bf906f09f0c6de8d5599d628d02e81f33c3f93b0b6755b524f3a80945` |
| `nixon_1973.xlsx` | 13,161 | `2923240378678b5fca2b9dd787b254aa5b96bb2bf605eba98526808dacd84a97` |
| `roosevelt_1941.xlsx` | 13,385 | `3e9a963d39efd24d07f46fa29688ca98f9c3620fefc4dca30494726b501251e4` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
