import struct
import lzma
from PIL import Image

def decode_image_to_file(image_filepath, output_filepath):
    """Extracts and decompresses the original file from an RGB PNG image."""
    try:
        img = Image.open(image_filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"The image file '{image_filepath}' does not exist.")

    if img.mode != 'RGB':
        raise ValueError("Image mode is not RGB. Data is likely corrupted.")

    full_data = img.tobytes()

    magic_bytes = full_data[0:3]
    if magic_bytes != b'B2Z':
        raise ValueError("Invalid magic bytes. This is not a recognized B2Z compressed image.")

    compressed_size = struct.unpack('>Q', full_data[3:11])[0]

    start_index = 11
    end_index = 11 + compressed_size
    actual_compressed_data = full_data[start_index:end_index]

    # Decompress back to the exact original payload
    try:
        original_data = lzma.decompress(actual_compressed_data)
    except lzma.LZMAError:
        raise ValueError("LZMA decompression failed. The payload is corrupted.")

    with open(output_filepath, 'wb') as f:
        f.write(original_data)

    return len(original_data)