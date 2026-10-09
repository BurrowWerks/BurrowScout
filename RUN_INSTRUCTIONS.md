# BurrowScout Run Instructions

## Ubuntu / WSL

From the BurrowScout project directory:

```bash
cd /mnt/b/Development/Projects/Learning/Python/BurrowScout
```

Activate the WSL virtual environment:

```bash
source .venv-wsl/bin/activate
```

The terminal should display:

```text
(.venv-wsl)
```

## Install Dependencies

```bash
python -m pip install requests beautifulsoup4 pytest
```

## Run BurrowScout

```bash
python sites.py
```

A successful run will retrieve the source, validate it, parse records, create
metadata, and write a JSON output file to:

```text
data/i_work_for_sa/
```

## Run Tests

From the project root:

```bash
python -m pytest -v
```

The current fixture is:

```text
tests/fixtures/i_work_for_sa.html
```

## Deactivate Environment

```bash
deactivate
```

## Windows PowerShell

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run:

```powershell
python sites.py
```

Tests:

```powershell
python -m pytest -v
```
