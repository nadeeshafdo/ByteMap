import argparse
import sys
from comp import encode_file_to_image
from decomp import decode_image_to_file

def main():
    parser = argparse.ArgumentParser(
        description="ByteMap: A modular Binary-to-PNG Encoder and Decoder. (Not a compression tool)",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'mode', 
        choices=['encode', 'decode'], 
        help="The operation to perform.\n  encode: Convert a file to a PNG image.\n  decode: Extract the original file from a PNG image. (No compression, just encoding)"
    )
    parser.add_argument('input', help="Path to the source file.")
    parser.add_argument('output', help="Path to the destination file.")

    args = parser.parse_args()

    try:
        if args.mode == 'encode':
            orig_size, comp_size, width, height = encode_file_to_image(args.input, args.output)
            print(f"[SUCCESS] Encoded {orig_size} bytes into a {width}x{height} PNG: {args.output}")
            print("[INFO] Note: This is not compression. PNG output may be larger than the original file.")

        elif args.mode == 'decode':
            file_size = decode_image_to_file(args.input, args.output)
            print(f"[SUCCESS] Decoded {file_size} bytes to: {args.output}")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()