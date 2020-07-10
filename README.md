# Generate Synthetic Images
Repository for reproducing synthetic transformations

## Install pip Dependencies
`pip install requirements.txt`

## Usage
Run `python synthesize.py` with necessary flags to generate individual transformations.

### Reproduce Digital and Photographic Dataset Generation
Digital Synthetic: `python synthesize.py --perturbation random-digital`  
Photographic Synthetic: `python synthesize.py --perturbation glare_matte --perturbation2 moire --perturbation3 tilt`  

### Arguments
`src_csv` Absolute path to source data csv.  
`dst_dir` Destination directory for synthesized data.  
`perturbation` Kind of perturbation to apply, required parameter.  
Choices: moire, blur, motion, glare_matte, glare_glossy, tilt, brightness_up, brightness_down, contrast_up, contrast_down, identity, random-digital, rotation, translation.  
`level` Severity of the perturbation. Default: 1.  
Choices: 1, 2, 3, 4  
`split` Data set split (train, valid, test). Note the split must be in the path for src_csv. Default: train.  

### Other Optional Arguments
`perturbation2` Applies the given perturbation after `perturbation`  
`perturbation3` Applies the given perturbation after `perturbation2`  

### Notes
For most transformations, the bottleneck is reading/writing image files. As a result, the script makes use of Python's parallel processing.
