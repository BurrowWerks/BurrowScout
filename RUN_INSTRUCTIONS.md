# BurrowScout Run Instructions

BurrowScout 0.1.0 requires Python 3.12 or later.

The currently verified development environment is:

- WSL/Linux
- Python 3.14.4
- pytest 9.1.1

Run all commands from the BurrowScout project root unless stated otherwise.

## Dependency installation

For the 0.1.0 development/test environment, install dependencies from the
repository's pinned `requirements.txt` file:

```bash
python -m pip install -r requirements.txt
```

`pyproject.toml` declares BurrowScout's direct runtime dependencies. The
`requirements.txt` file records the tested development environment, including
pytest and resolved supporting packages.

## Ubuntu / WSL

Open WSL and change to the directory where you cloned or downloaded
BurrowScout.

For example:

```bash
cd /path/to/BurrowScout
```

The path above is only an example. Use the actual path to your local checkout.

### Create the WSL virtual environment

```bash
python -m venv .venv-wsl
```

### Activate the WSL virtual environment

```bash
source .venv-wsl/bin/activate
```

The terminal should now show the active environment, for example:

```text
(.venv-wsl)
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run BurrowScout

```bash
python main.py
```

A successful run retrieves the configured I WORK FOR SA search results,
validates the responses, parses job records, creates run metadata, and writes a
JSON output file under:

```text
data/i_work_for_sa/
```

### Run the test suite

```bash
python -m pytest -v
```

The test suite uses offline fixtures and controlled fake HTTP responses where
appropriate. Fixture files are stored under:

```text
tests/fixtures/
```

### Deactivate the environment

```bash
deactivate
```

## Windows PowerShell

Open PowerShell and change to the directory where you cloned or downloaded
BurrowScout.

For example:

```powershell
cd C:\path\to\BurrowScout
```

The path above is only an example. Use the actual path to your local checkout.

### Create the Windows virtual environment

```powershell
python -m venv .venv
```

### Activate the Windows virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents the activation script from running because of the local
execution policy, use an appropriate PowerShell execution-policy setting for
your environment before retrying activation.

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Run BurrowScout

```powershell
python main.py
```

Output is written under:

```text
data/i_work_for_sa/
```

### Run the test suite

```powershell
python -m pytest -v
```

### Deactivate the environment

```powershell
deactivate
```

## Notes

- Windows and WSL use separate virtual environments because they contain
  platform-specific executables and installed packages.
- Do not copy or reuse the Windows `.venv` from WSL, or the WSL `.venv-wsl`
  from Windows.
- The WSL/Linux environment listed at the top of this document is the
  currently recorded verified environment for BurrowScout 0.1.0.
- Run BurrowScout from the project root so relative paths such as
  `data/i_work_for_sa/` resolve as expected.
