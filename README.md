# Generate Synthetic Images
Repo for reproducing synthetic transformations

## Install pip Dependencies
`pip install requirements.txt`

## Usage
Run `synthesize.py` to generate the transformations.

### Arguments
`src_csv` Absolute path to source data csv
`dst_dir` Destination directory for synthesized data
`perturbation` Kind of perturbation to apply
`level` Severity of the perturbation
`split` Data set split (train, valid, test). Note the split must be in the path for src_csv

### Other Optional Arguments
`perturbation2` Applies the given perturbation after `perturbation`
`perturbation3` Applies the given perturbation after `perturbation2`
