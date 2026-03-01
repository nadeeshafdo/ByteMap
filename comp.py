import math
import struct
import lzma
from PIL import Image

def encode_data_to_image(raw_data: bytes, output_image_path: str):
    """Compresses and encodes raw bytes into a 24-bit RGB PNG image."""
    compressed_data = lzma.compress(raw_data, preset=lzma.PRESET_EXTREME)
    compressed_size = len(compressed_data)

    magic_bytes = b'B2Z'
    size_bytes = struct.pack('>Q', compressed_size)
    header = magic_bytes + size_bytes

    full_data = bytearray(header + compressed_data)

    total_bytes = len(full_data)
    total_pixels = math.ceil(total_bytes / 3)

    width = min(4096, max(1, total_pixels))  
    height = math.ceil(total_pixels / width) if width > 0 else 1

    required_bytes = width * height * 3
    padding_needed = required_bytes - total_bytes
    full_data.extend(b'\x00' * padding_needed)

    img = Image.frombytes('RGB', (width, height), bytes(full_data))
    img.save(output_image_path, 'PNG')

    return len(raw_data), compressed_size, width, height

def encode_file_to_image(input_filepath, output_image_path):
    """Reads a file and passes it to the core encoder."""
    try:
        with open(input_filepath, 'rb') as f:
            raw_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{input_filepath}' does not exist.")
        
    return encode_data_to_image(raw_data, output_image_path)