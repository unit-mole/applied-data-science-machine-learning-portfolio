# Project Summary — U.S. Presidential Inaugural Speech Analysis

| Item | Verified content |
|---|---|
| Business objective | Compare lexical structure, readability, distinctive terms, similarity, and exploratory topics across three inaugural speeches. |
| Problem type | Small-corpus exploratory NLP |
| Dataset | The 1941 Roosevelt, 1961 Kennedy, and 1973 Nixon inaugural addresses stored as three workbooks. |
| Core methods | Corpus-quality audit, tokenization, lexical diversity, approximate Flesch readability, unigram/bigram TF-IDF, cosine similarity, distinctive-term analysis, and sentence-level NMF topics. |
| Final result | Kennedy 1961 and Nixon 1973 are the most similar tested pair by unigram/bigram TF-IDF cosine similarity (0.114), while topic and readability outputs remain exploratory. |
| Decision supported | Locate lexical differences for closer human reading rather than automate historical judgment. |
| Primary evidence | `reports/figures/speech_analysis_evidence.png` |
| Executed notebook | `notebooks/01_end_to_end_analysis.ipynb` |

## One-minute explanation

Kennedy 1961 and Nixon 1973 are the most similar tested pair by unigram/bigram TF-IDF cosine similarity (0.114), while topic and readability outputs remain exploratory. The implementation deliberately preserves the relevant entity, time, or train/test boundary and reports limitations instead of optimizing for an impressive-looking score.

## Review order

1. Read the executive summary in `README.md`.
2. Inspect the primary figure and comparison table.
3. Open the executed notebook for data and diagnostic evidence.
4. Review `src/analysis.py` for the reusable implementation.
5. Inspect `reports/metrics.json` for machine-readable values.
