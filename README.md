# ByteMap

ByteMap is a playful software project that explores the concept of storing arbitrary data by converting it into images and applying advanced (not really 🙂) lossless compression techniques. While the project is not intended for any production use, it serves as a fun experiment in data encoding, image processing, and compression.

## Features

- **Data-to-Image Conversion**: Transforms binary data into image representations.
- **Lossless Compression**: Applies advanced lossless compression to minimize storage size (Ahh.. near future 🙂?) while maintaining data integrity.
- **Decompression**: Recovers the original data from the compressed image.
- **Simple CLI**: Includes command-line tools for compressing and decompressing files.

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

### Compress a File

```bash
python main.py compress <input_file> <output_image>
```

### Decompress a File

```bash
python main.py decompress <input_image> <output_file>
```

## Example

```bash
python main.py compress secret.txt secret.png
python main.py decompress secret.png recovered.txt
```

## How It Works (Sort Of)

1. **Compression**: Reads the input file, encodes the data as pixel values in an image, and saves the image using a lossless format.
2. **Decompression**: Reads the image, decodes the pixel values back into the original data, and writes it to the output file.

> **Note:** This project is for entertainment and educational purposes only. It is not a serious or efficient solution for data storage or compression.

## Requirements

- Python 3.7+
- See `requirements.txt` for dependencies.

## Disclaimer

ByteMap is not a real data storage or compression solution. Use at your own risk, and enjoy the code!
