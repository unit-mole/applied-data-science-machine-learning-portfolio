# Data Documentation — Insurance Claim Propensity Modeling

## Scope

3,000 policy rows with demographic, agency, product, destination, duration, sales, commission, channel, and claim fields.

## Provenance and terms

Bundled in the original repository; the upstream sampling frame, collection process, and redistribution terms are not documented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `insurance_claims.csv` | 183,438 | `989cd34d3505baf1bd6d7b515ec0615a74f7c1c45a18480a3b021d31148a9fc0` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
