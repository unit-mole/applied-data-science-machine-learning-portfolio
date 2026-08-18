# Repository Architecture

`projects/` contains the 13 self-contained case studies. `portfolio_lib/` contains shared metric, modeling, and reporting helpers. `scripts/` generates notebook content, executes notebooks in isolated processes, checks the runtime, and compiles portfolio-level reports. `validate_portfolio.py` enforces the delivery contract; `run_all.py` orchestrates the complete rebuild.

Generated evidence is deliberately committed: notebook outputs provide an auditable analysis trail, while `reports/metrics.json`, CSV tables, and PNG figures make results easy to inspect and reuse.
