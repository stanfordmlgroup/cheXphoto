![LOGO](/img/CheXphoto.png)

Repository referenced in the paper, "CheXphoto: 10,000+ Smartphone Photos and Synthetic Photographic Transformations of Chest X-rays for Benchmarking Deep Learning Robustness," for generating natural and synthetic transformations. To download the full dataset or view and submit to the leaderboard, visit the [CheXphoto website](https://stanfordmlgroup.github.io/competitions/chexphoto/).

### Table of Contents
* [Generate Natural Transformations with CheXpeditor](#natural)
* [Generate Synthetic Transformations](#synthetic)
* [License](#license)
* [Citing](#citing)

---

<a name="natural"></a>
## Generating Natural Transformations with CheXpeditor

---

<a name="synthetic"></a>
## Generating Synthetic Transformations

The transformations were generated with Python version 3.7.6.  
`pip install -r requirements.txt`

### Usage

```
Usage: python synthesize.py [OPTIONS]

Options:
    --src_csv      Absolute path to source data csv.
    --dst_dir      Destination directory for synthesized data.
    --perturbation Kind of perturbation to apply, required parameter.
    --level        Severity of the perturbation. Default: 1.
    --split        Data set split
```

### Reproduce Digital and Photographic Dataset Generation

Digital Synthetic:

```
python synthesize.py --perturbation random-digital
```

Photographic Synthetic:

```
python synthesize.py --perturbation glare_matte --perturbation2 moire --perturbation3 tilt
```

### Arguments

- Perturbation Choices:
  - moire
  - blur
  - motion
  - glare_matte
  - glare_glossy
  - tilt
  - brightness_up
  - brightness_down
  - contrast_up
  - contrast_down
  - identity
  - random-digital
  - rotation
  - translation
- Level Choices: 1, 2, 3, 4
  - default: 1
- Split Choices: train, valid, test
  - Note the split must be in the path for src_csv.
  - default: train

### Other Optional Arguments

`perturbation2` Applies the given perturbation after `perturbation`  
`perturbation3` Applies the given perturbation after `perturbation2`

### Notes

For most transformations, the bottleneck is reading/writing image files. As a result,the script makes use of Python's parallel processing.

It is expected that `src_csv` contains a column which can be parsed by pandas as `Path`, containing the paths to each of the images to be transformed.

---

<a name="license"></a>
## License

This repository is made publicly available under the MIT License.

<a name="citing"></a>
## Citing

If you are using the CheXphoto dataset, please cite this paper:

```
@inproceedings{phillips20chexphoto,
  title={CheXphoto: 10,000+ Smartphone Photos and Synthetic Photographic Transformations of Chest X-rays for Benchmarking Deep Learning Robustness},
  author={Phillips, Nick and Rajpurkar, Pranav and Sabini, Mark and Krishnan, Rayan and Zhou, Sharon and Pareek, Anuj and Phu, Nguyet Minh and Wang, Chris and Ng, Andrew and Lungren, Matthew and others},
  year={2020}
}
```
