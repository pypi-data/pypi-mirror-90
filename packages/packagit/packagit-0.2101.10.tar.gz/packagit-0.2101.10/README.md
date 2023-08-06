![test](https://github.com/davips/packagit/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/davips/packagit/branch/main/graph/badge.svg)](https://codecov.io/gh/davips/packagit)

# packagit
Increment version, create and push tag for release on github and pypi

Write your first version inside setup.py in the form

```python
VERSION = "0.2101.0"  # major.YYMM.minor
```

Copy the workflow file (release.yml) to .github/workflows of your rpoject repository.

Run at the shell prompt

```bash
packagit 0  # 0 is the major version number, the minor number will be automatically incremented.
```

