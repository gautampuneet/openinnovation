import numpy as np
from src.utils.image_frame_utils import ImageProcessor

def test_resize_image():
    original_width = 200
    new_width = 150
    pixel_values = np.random.randint(0, 256, size=(1, original_width)).tolist()
    resized_values = ImageProcessor().resize_image(pixel_values, original_width, new_width)
    assert resized_values.shape[1] == new_width

def test_apply_custom_colormap():
    pixels = np.random.randint(0, 256, size=(1, 150)).flatten().tolist()
    colored_image = ImageProcessor().apply_custom_colormap(pixels)
    assert len(colored_image[0][0]) == 3

