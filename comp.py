import math
import struct
import lzma
from PIL import Image

def encode_file_to_image(input_filepath, output_image_path):
    """Compresses and encodes a file into a 24-bit RGB PNG image."""
    try:
        with open(input_filepath, 'rb') as f:
            raw_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{input_filepath}' does not exist.")

    # Compress the payload mercilessly
    compressed_data = lzma.compress(raw_data, preset=lzma.PRESET_EXTREME)
    compressed_size = len(compressed_data)

    # Metadata Header: Magic bytes 'B2Z' + 64-bit unsigned integer
    magic_bytes = b'B2Z'
    size_bytes = struct.pack('>Q', compressed_size)
    header = magic_bytes + size_bytes

    full_data = bytearray(header + compressed_data)

    total_bytes = len(full_data)
    total_pixels = math.ceil(total_bytes / 3)

    # Use minimal bounding rectangle (width x height)
    width = min(4096, total_pixels)  # Limit width for practical image sizes
    height = math.ceil(total_pixels / width)

    required_bytes = width * height * 3
    padding_needed = required_bytes - total_bytes
    full_data.extend(b'\x00' * padding_needed)

    img = Image.frombytes('RGB', (width, height), bytes(full_data))
    img.save(output_image_path, 'PNG')

    return len(raw_data), compressed_size, width, height