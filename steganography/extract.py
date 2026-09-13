from PIL import Image

END_MARKER = "#####END#####"


def binary_to_text(binary_data):
    text = ""

    for i in range(0, len(binary_data), 8):

        byte = binary_data[i:i + 8]

        if len(byte) == 8:
            text += chr(int(byte, 2))

    return text


def extract_data(image_path):

    image = Image.open(image_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    pixels = image.load()

    width, height = image.size

    binary_data = ""

    for y in range(height):

        for x in range(width):

            pixel = pixels[x, y]

            for channel in range(3):

                binary_data += str(pixel[channel] & 1)

    extracted_text = binary_to_text(binary_data)

    end_index = extracted_text.find(END_MARKER)

    if end_index != -1:
        return extracted_text[:end_index]

    return ""