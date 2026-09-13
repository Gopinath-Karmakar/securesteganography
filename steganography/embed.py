from PIL import Image


END_MARKER = "#####END#####"


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def calculate_capacity(image_path):
    image = Image.open(image_path)

    width, height = image.size

    total_pixels = width * height

    total_bits = total_pixels * 3

    total_characters = total_bits // 8

    return total_characters


def embed_data(image_path, secret_data, output_path):

    image = Image.open(image_path)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    secret_data += END_MARKER

    binary_data = text_to_binary(secret_data)

    width, height = image.size

    capacity = width * height * 3

    if len(binary_data) > capacity:
        raise ValueError(
            "Message exceeds image embedding capacity."
        )

    pixels = image.load()

    data_index = 0

    for y in range(height):

        for x in range(width):

            pixel = list(pixels[x, y])

            for channel in range(3):

                if data_index < len(binary_data):

                    pixel[channel] = (
                        pixel[channel] & ~1
                    ) | int(binary_data[data_index])

                    data_index += 1

            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_data):

                image.save(output_path)

                return True

    image.save(output_path)

    return True