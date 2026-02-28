import math
import struct
from PIL import Image

def encode_file_to_image(input_filepath, output_image_path):
    """Encodes a file into a 24-bit RGB PNG image."""
    try:
        with open(input_filepath, 'rb') as f:
            file_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"The input file '{input_filepath}' does not exist.")
    
    file_size = len(file_data)
    
    # Metadata Header: Magic bytes 'B2P' + 64-bit unsigned integer
    magic_bytes = b'B2P'
    size_bytes = struct.pack('>Q', file_size)
    header = magic_bytes + size_bytes
    
    full_data = bytearray(header + file_data)
    
    total_bytes = len(full_data)
    total_pixels = math.ceil(total_bytes / 3)
    
    width = math.ceil(math.sqrt(total_pixels))
    height = width 
    
    required_bytes = width * height * 3
    padding_needed = required_bytes - total_bytes
    full_data.extend(b'\x00' * padding_needed)
    
    img = Image.frombytes('RGB', (width, height), bytes(full_data))
    img.save(output_image_path, 'PNG')
    
    return file_size, width, height