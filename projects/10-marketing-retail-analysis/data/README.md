# Data Documentation — Cafe Marketing and Retail Analytics

## Scope

145,830 cafe line items covering 69,982 bills and one year of activity.

## Provenance and terms

Bundled in the original repository; business identity, geography, currency, and redistribution terms are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `cafe_transactions.xlsx` | 8,281,913 | `ea3c0b8e8a7d9d4bccc4cba5a58778516f5119931df4a9438ba500ac84d662fa` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
