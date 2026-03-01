import argparse
import sys
from comp import encode_file_to_image, encode_data_to_image
from decomp import decode_image_to_file, decode_image_to_data

def main():
    parser = argparse.ArgumentParser(
        description="ByteMap: A modular Binary-to-PNG Encoder and Decoder.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'mode', 
        choices=['encode', 'decode'], 
        help="The operation to perform.\n  encode: Convert a file or raw {data} to a PNG image.\n  decode: Extract the original file/data from a PNG image."
    )
    
    parser.add_argument('input', help="Path to the source file, or {string} for inline text.")
    
    # nargs='?' makes the output argument optional, permitting stdout decoding
    parser.add_argument('output', nargs='?', help="Path to the destination file. Optional when decoding to console.")

    args = parser.parse_args()

    try:
        if args.mode == 'encode':
            if not args.output:
                print("main.py: error: the following arguments are required: output when encoding")
                sys.exit(1)

            # Intercept inline string format
            if args.input.startswith('{') and args.input.endswith('}'):
                raw_string = args.input[1:-1]
                encode_data_to_image(raw_string.encode('utf-8'), args.output)
                print(f"[INFO] The input data '{raw_string}' saved to '{args.output}' file.")
            else:
                orig_size, comp_size, width, height = encode_file_to_image(args.input, args.output)
                print(f"[SUCCESS] Encoded {orig_size} bytes into a {width}x{height} PNG: {args.output}")
                print("[INFO] Note: This is not compression. PNG output may be larger than the original file.")

        elif args.mode == 'decode':
            if args.output:
                # File-to-File
                file_size = decode_image_to_file(args.input, args.output)
                print(f"[SUCCESS] Decoded {file_size} bytes to: {args.output}")
            else:
                # File-to-Console
                raw_bytes = decode_image_to_data(args.input)
                try:
                    text_data = raw_bytes.decode('utf-8')
                    print(f"[DATA] {text_data}")
                except UnicodeDecodeError:
                    print(f"[DATA] <Non-printable binary data: {len(raw_bytes)} bytes>")

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()