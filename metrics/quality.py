import numpy as np
from PIL import Image
import math


def load_rgb_image(image_path):
    """
    Load an image and convert it to RGB
    so both images have the same number of channels.
    """
    image = Image.open(image_path).convert("RGB")
    return np.array(image, dtype=np.float64)


def calculate_mse(original_image_path, stego_image_path):

    original = load_rgb_image(original_image_path)
    stego = load_rgb_image(stego_image_path)

    mse = np.mean((original - stego) ** 2)

    return mse


def calculate_psnr(original_image_path, stego_image_path):

    mse = calculate_mse(original_image_path, stego_image_path)

    if mse == 0:
        return float("inf")

    max_pixel = 255.0

    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))

    return psnr


def image_capacity(image_path):

    image = Image.open(image_path).convert("RGB")

    width, height = image.size

    total_pixels = width * height

    total_bits = total_pixels * 3

    total_characters = total_bits // 8

    return {
        "Width": width,
        "Height": height,
        "Pixels": total_pixels,
        "Bits": total_bits,
        "Characters": total_characters
    }