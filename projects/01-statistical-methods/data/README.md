# Data Documentation — Statistical Methods for Decision-Making

## Scope

440 wholesale customers, 62 survey respondents, and 36 shingle rows across three CSV files.

## Provenance and terms

Wholesale data aligns with the UCI Wholesale Customers dataset. Survey and shingle collection protocols and reuse terms were not supplied in the original project.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `shingles.csv` | 374 | `b9a12bc5aee1fb608db8eb15b24150e20378129b36c828f474428450bcc8ceaf` |
| `university_survey.csv` | 4,863 | `4ff41af9f9795d3d2aa246b3fe0b860b70e1f7c252b8e815d18ff05170d4f05f` |
| `wholesale_customers.csv` | 20,475 | `0b893d36b4a7abceb62156694938d9723cafdb972807f63cff201af957f4c1b9` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
