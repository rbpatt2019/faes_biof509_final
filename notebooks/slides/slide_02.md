## Command line notebooks!

Shout out to Martin's nbless package!

```bash
nbless notebooks/slides/slide_* -o notebooks/index.ipynb
nbdeck notebooks/index.ipynb
nbconv notebooks/index.ipynb -e slides -o index.html
cp index.html reports/index.html
```

