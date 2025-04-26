# baker

A Python application for creating boilerplate project directories for new Python projects. Will create virtual environments, subdirectories, and write file templates (eg, README.md).

## Installation

Clone the repo:

```bash
git clone https://github.com/notoriouslogank/baker.git
cd baker
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

For a simple example:

```bash
python3 baker.py example_project
```

More complicated setup:
```bash
python3 baker.py example_project -d . --no-venv --git -s example_subdirectory
```

For detailed information, use baker's builtin help function:

```bash
python3 baker.py --help
```
