# Data Documentation — Salary Factor Analysis and College Admissions PCA

## Scope

40 salary observations and 777 colleges with 17 numeric admissions and institutional indicators.

## Provenance and terms

College data corresponds to the ISLR College dataset; the small salary dataset's sampling process and license are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `college_admissions.csv` | 72,803 | `d57bbc2f3edf6acb077ccd1e1d20228b56b6adde6fffd91cb1ce108e6eb227ec` |
| `salary_data.csv` | 1,278 | `457fa1f5a40ee9dec5fe29b3a3efab2832a2873282a37c214983d01991a14a0e` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
