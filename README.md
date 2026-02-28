# ByteMap

ByteMap is a playful software project that explores the concept of storing arbitrary data by converting it into images. This project is not a compression tool, nor is it intended for steganography or secure storage. It is a fun experiment in data encoding and image processing, and the resulting images are not smaller than the original files.

## Features

- **Data-to-Image Conversion**: Transforms binary data into image representations.
- **Encoding**: Converts binary data into image representations.
- **Decoding**: Recovers the original data from the encoded image.
- **Simple CLI**: Includes command-line tools for encoding and decoding files.

## Project Structure

- `main.py` — Entry point for the CLI interface.
- `comp.py` — Handles data-to-image conversion and compression logic.
- `decomp.py` — Handles image-to-data conversion and decompression logic.
- `requirements.txt` — Python dependencies.

## Setting Up

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Encode a File

```bash
python main.py encode <input_file> <output_image>
```

### Decode a File

```bash
python main.py decode <input_image> <output_file>
```

## Example

```bash
python main.py encode secret.txt secret.png
python main.py decode secret.png recovered.txt
```

## How It Works (Sort Of)

1. **Encoding**: Reads the input file, encodes the data as pixel values in an image, and saves the image using a lossless format.
2. **Decoding**: Reads the image, decodes the pixel values back into the original data, and writes it to the output file.

> **Note:** This project is for entertainment and educational purposes only. It is not a serious or efficient solution for data storage, compression, or steganography. The PNG output is typically larger than the original file and is not intended for real-world use cases.

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies.

## Disclaimer

ByteMap is not a real data storage or compression solution. Use at your own risk, and enjoy the code!
