# HDF5 Cleaner

This Python tool creates a copy of an HDF5 file, removing all datasets that have at least one dimension of size zero (i.e. empty datasets). The original group structure and dataset attributes are preserved.

## Features

- Removes all empty datasets (e.g. shape `(0,)`, `(0, 128)`, etc.)
- Retains non-empty datasets, group hierarchy, and attributes
- Simple command-line interface (CLI)
- Uses `h5py` for fast and reliable HDF5 operations

## Requirements

Install dependencies with:

```
pip install -r requirements.txt
```

## Usage
Run the script with:

```
python main.py --input path/to/original.h5 --output path/to/cleaned.h5
```

## Example

```
python main.py --input data/original/myfile.h5 --output data/cleaned/myfile_cleaned.h5
```
