# Data Documentation — Participant-Safe Parkinson's Voice Classification

## Scope

195 recordings, 22 acoustic features, and 32 derived participant identifiers.

## Provenance and terms

Matches the UCI Parkinsons voice dataset; participant IDs are derived from the recording-name field.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `parkinsons.csv` | 37,901 | `0736fa3a8ac098c4fed4312723705adff4a2aebc78f52971c3883fb33401f5b3` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
