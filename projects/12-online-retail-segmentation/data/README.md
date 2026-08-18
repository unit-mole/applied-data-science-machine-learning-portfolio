# Data Documentation — Online Retail Customer Segmentation

## Scope

541,909 UCI Online Retail transaction rows from December 2010 through December 2011.

## Provenance and terms

UCI Online Retail dataset; preserve UCI attribution and verify source-specific reuse terms before redistribution.

The MIT license at repository root applies to code, not automatically to source data. Verify dataset-specific terms before redistribution or production reuse.

## Local-file manifest

| File | Bytes | SHA-256 |
|---|---:|---|
| `online_retail.xlsx` | 23,715,344 | `43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d` |

## Unit of analysis and limitations

The primary notebook identifies the analytical unit, target where applicable, time coverage, missingness, duplicates, invalid ranges, identifiers, and leakage risks. Cleaning rules are explicit in `src/analysis.py` and their row impacts are saved in `reports/tables/`.
