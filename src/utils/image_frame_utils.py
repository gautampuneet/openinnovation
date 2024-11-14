import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class ImageProcessor:

    @staticmethod
    def resize_image(pixel_values, original_width=200, new_width=150):
        image = np.array(pixel_values, dtype=np.uint8).reshape(-1, original_width)
        image_pil = Image.fromarray(image)
        aspect_ratio = image_pil.width / float(image_pil.height)
        new_height = math.ceil(new_width / aspect_ratio)
        image_resized = image_pil.resize((new_width, new_height), Image.LANCZOS)
        return np.array(image_resized)

    @staticmethod
    def apply_custom_colormap(pixels, width=150):
        image = np.array(pixels).reshape(-1, width)
        colormap = plt.cm.viridis
        colored_image = colormap(image)
        color_applied_rgb = (colored_image[:, :, :3] * 255).astype(np.uint8)
        return color_applied_rgb.tolist()
    