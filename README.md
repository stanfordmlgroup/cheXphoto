![LOGO](/img/CheXphoto.png)

Repository referenced in the paper, "CheXphoto: 10,000+ Smartphone Photos and Synthetic Photographic Transformations of Chest X-rays for Benchmarking Deep Learning Robustness," for generating natural and synthetic transformations. To download the full dataset or view and submit to the leaderboard, visit the [CheXphoto website](https://stanfordmlgroup.github.io/competitions/chexphoto/).

### Table of Contents

- [Prerequisites](#prereqs)
- [Generate Natural Transformations with CheXpeditor](#natural)
- [Generate Synthetic Transformations](#synthetic)
- [License](#license)
- [Citing](#citing)

---

<a name="prereqs"></a>

## Prerequisites

Python 3.7+ should be sufficient to run the code in the repo. The natural transformation code has been tested with Python 3.8.2, while the synthetic transformations were generated using Python 3.7.6.

Before starting, please install the repo Python requirements using the following command:
```
pip install -r requirements.txt
```

Note the following additional requirements for generating **natural transformations**:
* For **manual** photo acquisition, any phone with a camera is sufficient.
* For **automatic** photo acquisition, a relatively recent Android smartphone is required since it must run the CheXpeditor app. In addition, a tripod is strongly recommended for long periods of operation. Please see additional details in the [usage instructions for auto mode](#auto).

<a name="natural"></a>

## Generating Natural Transformations with CheXpeditor

We developed CheXpeditor as a workflow to expedite and automate the process of taking photos of chest x-rays. CheXpeditor offers two modes of operation:

- **Manual mode**, which iterates over a CSV at a given rate, allowing the user to manually capture photographs on their device
- **Auto mode**, which utilizes the custom CheXpeditor app to remotely and robustly trigger the phone's camera. This was used to capture the Nokia10k dataset.

### Usage (Manual Mode)

In manual mode, the CheXpeditor client iterates through a CSV and shows x-rays at a specified rate, or upon receiving a keypress. The user manually triggers the camera when the image changes. Extra care must be taken to properly correlate the photos of the x-rays to the original x-rays in order to correctly assign the respective labels.

<details>
  <summary>Detailed Instructions (Manual Mode)</summary>
  
The script `chexpeditor_collect_manual.py` will run CheXpeditor in manual mode. The usage is documented by running `python chexpeditor_collect_manual.py --help`, which is reproduced below:

```
python chexpeditor_collect_manual.py [OPTIONS]

Options:
--csv_path			Path to data CSV
--data_dir   		The directory in which CheXphoto is located
--row_start    		Row index of the first image to load (inclusive). 0 is first image
--row_end     		Row index of the last entry to load (exclusive). Omit to load all entries until end.
--screen_height 	Height (in px) of the screen
--screen_width 		Width (in px) of the screen
--delay        		Interval in between images (in ms). Omit to require a keypress to advance.
```

More information on usage (and sample invocations) is available in the file-level docstring for `chexpeditor_collect_manual.py`.

</details>

<a name="auto"></a>

### Usage (Auto Mode)

In auto mode, the CheXpeditor client communicates with the CheXpeditor app running on a smartphone to remotely and robustly trigger the phone's camera. As the image's metadata is embedded in the filename, auto mode also provides functionality to batch postprocess the CheXpeditor output to create a CSV and dataset in CheXphoto format.

<details>
  <summary>Detailed Instructions (Auto Mode)</summary>

#### Auto Mode Setup

1. Install the CheXpeditor application on your smartphone. As of now, we only support relatively recent Android phones (Android 8+, equivalently API level 26+). There are two installation methods:
   - **Via APK**. The CheXpeditor APK is available in `chexpeditor/server/chexpeditor-server.apk`. You can copy it directly to your phone and open it from the File Manager to install. **FOR YOUR SECURITY, do not install the APK from any other source other than this repo!** If you are unsure whether an APK you have received is safe, we also provide the Android Studio project which can be used to build the CheXpeditor app.
   - **Via build from Android Studio**. In the case the application fails to install or function on your device, we have provided the Android Studio project which contains the necessary resources to build the CheXpeditor app.
2. Once installed, you may need to set the permissions for the CheXpeditor app to allow access to "Storage" (for writing files) and "Camera" (for taking pictures). Insufficient permissions can cause the app to crash.
3. Use a tripod to mount the phone into a position in front of the monitor where an image will be visible. To test that the chest x-ray is fully in view, you can use manual mode to cycle through some images.
4. Make sure that your computer and the phone are on the **same network**. This will enable them to communicate and exchange metadata.

#### Running CheXpeditor Server & Client

Once setup is complete, you are ready to run CheXpeditor in auto mode with the following steps!

1. Start the CheXpeditor server (app) on your phone.

   - In the field for `row_start`, enter the row of your CSV that you would like to begin taking photos at.
   - Press the "Start" button. You should see a status message similar to `UDP Server is running on 10.2.1.103:4445`. This is the IP and port of the server. Save this information for the next step.

2. Start the CheXpeditor client on your computer.

   - The script `chexpeditor_collect_auto.py` will start the CheXpeditor client in auto mode. The usage is documented by running `python chexpeditor_collect_auto.py --help`, which is reproduced below:

     ```
     python chexpeditor_collect_auto.py [OPTIONS]

     Options:
       --csv_path 		Path to data CSV
       --data_dir		The directory in which CheXphoto is located
       --row_start 		Row index of the first image to load (inclusive). 0 is first image
       --row_end			Row index of the last entry to load (exclusive). Omit to load all entries until end.
       --screen_height	Height (in px) of the screen
       --screen_width 	Width (in px) of the screen
       --ip      	    IP address for CheXpeditor server
       --port			Port for CheXpeditor server
     ```

     More information on usage (and sample invocations) is available in the file-level docstring for `chexpeditor_collect_auto.py`.

   - One important thing to note is that the `--row_start` parameter passed into the script **must match** the `row_start` entered into the application UI. This ensures that the server and client are explicitly in sync.

   - If everything was successful, you should see the x-rays automatically advance on the computer monitor, as the CheXpeditor app automatically triggers the phone camera.

#### Creating a Dataset from CheXpeditor Output

After running through the images, any photos from CheXpeditor will be stored in the `/CheXpeditor/` folder on your phone. At this point, you can transfer them off your phone and onto your computer into any directory, which we will refer to as `--chexpeditor_export_dir`.

Given these images, the script `compile_csv_from_chexpeditor.py` will take the original CSV used to run the CheXpeditor client, and assign labels to the CheXpeditor photos using the metadata embedded in the filename. Additionally, it will generate a dataset in the CheXphoto format, along with the corresponding CSV. You can now use this dataset for training or evaluation. The usage is documented by running `python compile_csv_from_chexpeditor.py --help`, which is reproduced below:

```
python compile_csv_from_chexpeditor.py [OPTIONS]

Options:
  --src_csv_path				Path to original source CSV (--csv_path in collect_natural_auto.py)
  --src_row_start				Starting row of source data range (inclusive)
  --src_row_end					Ending row of source data range (exclusive)
  --chexpeditor_export_dir 		Local directory containing CheXpeditor outputs
  --dst_data_dir				Where the output images should be saved, preserving the original directory structure
  --dst_dataset_name			Name for generated dataset, which will be prepended to paths in destination CSV
  --dst_csv_path				Save location for the CSV of the transformed dataset
  --copy			         	Specify False to only generate a CSV
```

More information on usage (and sample invocations) is available in the file-level docstring for `compile_csv_from_chexpeditor.py`.

</details>

---

<a name="synthetic"></a>

## Generating Synthetic Transformations

`synthesize.py` is the key script for applying synthetic transformations to data. The implementations of the various synthetic transformations are available in the `transforms/` subfolder.

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

---

```
Perturbation Choices:
    moire, blur, motion, glare_matte, glare_glossy, tilt,
    brightness_up, brightness_down, contrast_up, contrast_down,
    identity, random-digital, rotation, translation

Level Choices:
    1, 2, 3, 4
    default: 1

Split Choices:
    train, valid, test
    default: train
    Note the split must be in the path for src_csv.
```

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
