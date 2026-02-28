import struct
from PIL import Image

def decode_image_to_file(image_filepath, output_filepath):
    """Decodes the RGB PNG image back into the exact original file."""
    try:
        img = Image.open(image_filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"The image file '{image_filepath}' does not exist.")

    if img.mode != 'RGB':
        raise ValueError("Image mode is not RGB. Data is likely corrupted.")
        
    full_data = img.tobytes()
    
    magic_bytes = full_data[0:3]
    if magic_bytes != b'B2P':
        raise ValueError("Invalid magic bytes. This is not a recognized B2P encoded image.")
        
    file_size = struct.unpack('>Q', full_data[3:11])[0]
    
    start_index = 11
    end_index = 11 + file_size
    actual_file_data = full_data[start_index:end_index]
    
    with open(output_filepath, 'wb') as f:
        f.write(actual_file_data)
        
    return file_size