# Data Documentation — Historical COVID-19 Next-Day Case Modeling

## Scope

19,496 country-date rows from December 2019 through May 2020 with cases, tests, policy, population, and demographic fields.

## Provenance and terms

Schema and period align with an early Our World in Data snapshot; exact snapshot checksum and redistribution history were not recorded in the original repository.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `covid.csv` | 2,998,763 | `04999b024586aafbbc4f07619b49e0701a42ea0572192ca694b696fe43685282` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
