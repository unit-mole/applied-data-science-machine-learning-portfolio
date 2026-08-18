# GitHub Push Guide

Run the full validation before publishing:

```powershell
cd D:\AI-Training\applied-data-science-portfolio-rebuilt
.\.venv\Scripts\Activate.ps1
python validate_portfolio.py
python -m unittest discover -s tests -v
```

Create and push the repository:

```powershell
git init
git branch -M main
git add .
git status
git commit -m "Publish executed applied data science portfolio"
git remote add origin https://github.com/unit-mole/applied-data-science-portfolio-rebuilt.git
git push -u origin main
```

If the remote already exists, use `git remote set-url origin <URL>` instead of `git remote add`. Do not commit `.venv`; it is excluded by `.gitignore`. After pushing, open **Actions** and confirm that both Python 3.12 and 3.13 validation jobs pass. Then open several notebooks on GitHub and confirm their charts and tables render.
