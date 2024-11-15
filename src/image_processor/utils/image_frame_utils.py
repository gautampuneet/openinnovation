import math
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from typing import List

class ImageProcessor:

    @staticmethod
    def resize_image(pixel_values: np.array, original_width: int = 200, new_width: int = 150) -> np.array:
        """
            Resizes a 2D array of pixel values to a new width while maintaining the aspect ratio.

            Args:
                pixel_values (np.array): A 2D array representing pixel values.
                original_width (int, optional): The width of the original image. Defaults to 200.
                new_width (int, optional): The desired width of the resized image. Defaults to 150.

            Returns:
                np.array: A 2D array of the resized pixel values.
        """
        image = np.array(pixel_values, dtype=np.uint8).reshape(-1, original_width)
        image_pil = Image.fromarray(image)
        aspect_ratio = image_pil.width / float(image_pil.height)
        new_height = math.ceil(new_width / aspect_ratio)
        image_resized = image_pil.resize((new_width, new_height), Image.LANCZOS)
        return np.array(image_resized)

    @staticmethod
    def apply_custom_colormap(pixels: List[int], width: int = 150) -> List[List[List[int]]]:
        """
            Applies a custom colormap to a 2D array of pixel values and converts it to RGB format.

            Args:
                pixels (List[int]): A flat list of pixel values to be converted.
                width (int, optional): The width of the image. Defaults to 150.

            Returns:
                List[List[List[int]]]: A 3D list representing the RGB pixel values after applying the colormap.
        """
        pixels = np.asarray(pixels, dtype=np.float32).reshape(-1, width)
        pixels = (pixels - np.min(pixels)) / (np.max(pixels) - np.min(pixels) + 1e-5)
        colormap = plt.cm.get_cmap("inferno")
        colored_image = colormap(pixels)  # Outputs RGBA normalized values
        # Convert to RGB and scale to 0-255 in one step
        color_applied_rgb = (colored_image[:, :, :3] * 255).astype(np.uint8)

        # Return NumPy array instead of a Python list for better performance downstream
        return color_applied_rgb.tolist()
    