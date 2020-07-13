"""Directory of all perturbations and levels."""

from transforms.moire import moire_mapping
from transforms.blur import blur_mapping
from transforms.motion import motion_mapping
from transforms.glare_matte import glare_matte_mapping
from transforms.glare_glossy import glare_glossy_mapping
from transforms.tilt import tilt_mapping
from transforms.brightness_up import brightness_up_mapping
from transforms.brightness_down import brightness_down_mapping
from transforms.contrast_up import contrast_up_mapping
from transforms.contrast_down import contrast_down_mapping
from transforms.identity import identity_mapping
from transforms.random_digital import random_digital_mapping
from transforms.rotation import rotation_mapping
from transforms.translation import translation_mapping
from transforms.exposure import exposure_mapping

PERTURBATIONS = {'moire': moire_mapping,
                 'blur': blur_mapping,
                 'motion': motion_mapping,
                 'glare_matte': glare_matte_mapping,
                 'glare_glossy': glare_glossy_mapping,
                 'tilt': tilt_mapping,
                 'brightness_up': brightness_up_mapping,
                 'brightness_down': brightness_down_mapping,
                 'contrast_up': contrast_up_mapping,
                 'contrast_down': contrast_down_mapping,
                 'identity': identity_mapping,
                 'random-digital': random_digital_mapping,
                 'rotation':rotation_mapping,
                 'translation':translation_mapping,
                 'exposure':exposure_mapping}
LEVELS = [1, 2, 3, 4]
