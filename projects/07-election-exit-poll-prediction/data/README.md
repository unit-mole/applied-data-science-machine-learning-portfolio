# Data Documentation — Retrospective Election Survey Classification

## Scope

1,525 historical survey rows with vote, age, leader ratings, economic assessments, Europe attitudes, knowledge, and gender.

## Provenance and terms

Bundled in the original repository; survey organization, weighting, sampling design, and license are undocumented.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `election_data.xlsx` | 77,826 | `af2bb5a60c1923c586e5447d487efb92b497cde50e0dee53791174cd76eb0a77` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
