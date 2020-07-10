"""Directory of all perturbations and levels."""

from moire import moire_mapping
from blur import blur_mapping
from motion import motion_mapping
from glare_matte import glare_matte_mapping
from glare_glossy import glare_glossy_mapping
from tilt import tilt_mapping
from brightness_up import brightness_up_mapping
from brightness_down import brightness_down_mapping
from contrast_up import contrast_up_mapping
from contrast_down import contrast_down_mapping
from identity import identity_mapping
from random_digital import random_digital_mapping
from rotation import rotation_mapping
from translation import translation_mapping
from exposure import exposure_mapping

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
