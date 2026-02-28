# Simple File-to-PNG Converter
#
# This script takes any file (audio, video, image, document, etc.),
# reads its raw binary data, splits it into 4-bit segments, and
# encodes each 4-bit segment as a pixel in a PNG image, where each
# pixel's RGBA channels are filled with 4 bits each from the data.
#
# Only Python 3 standard libraries are used.
#
# Usage: python3 comp.py <input_file> <output_image.png>

import sys
import math
import struct
import zlib

def file_to_4bit_segments(filepath):
	"""Read file as bytes and split into 4-bit segments."""
	with open(filepath, 'rb') as f:
		data = f.read()
	bits = []
	for byte in data:
		bits.append((byte >> 4) & 0xF)
		bits.append(byte & 0xF)
	return bits

def segments_to_rgba_pixels(segments):
	"""Group 4-bit segments into RGBA pixels (4 segments per pixel)."""
	pixels = []
	for i in range(0, len(segments), 4):
		rgba = [0, 0, 0, 0]
		for j in range(4):
			if i + j < len(segments):
				# Scale 4-bit value (0-15) to 8-bit (0-255)
				rgba[j] = segments[i + j] * 17
		pixels.append(tuple(rgba))
	return pixels

def make_png(width, height, pixels, output_path):
	"""Create a PNG file from RGBA pixel data using only stdlib."""
	# PNG file signature
	png_sig = b'\x89PNG\r\n\x1a\n'
	# Prepare raw image data (scanlines with filter byte 0)
	raw_data = bytearray()
	for y in range(height):
		raw_data.append(0)  # No filter
		for x in range(width):
			idx = y * width + x
			if idx < len(pixels):
				raw_data.extend(pixels[idx])
			else:
				raw_data.extend((0, 0, 0, 255))  # Pad with opaque black
	# Compress image data
	compressed = zlib.compress(bytes(raw_data), level=9)
	# Helper to create PNG chunks
	def png_chunk(chunk_type, data):
		chunk = struct.pack('>I', len(data))
		chunk += chunk_type
		chunk += data
		crc = zlib.crc32(chunk_type + data) & 0xffffffff
		chunk += struct.pack('>I', crc)
		return chunk
	# IHDR chunk
	ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
	# 8 bits per channel, RGBA, no interlace
	# Assemble PNG
	png = bytearray()
	png += png_sig
	png += png_chunk(b'IHDR', ihdr)
	png += png_chunk(b'IDAT', compressed)
	png += png_chunk(b'IEND', b'')
	with open(output_path, 'wb') as f:
		f.write(png)

def main():
	if len(sys.argv) != 3:
		print("Usage: python3 comp.py <input_file> <output_image.png>")
		sys.exit(1)
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	segments = file_to_4bit_segments(input_file)
	pixels = segments_to_rgba_pixels(segments)
	# Choose image size: make it as square as possible
	num_pixels = len(pixels)
	width = math.ceil(math.sqrt(num_pixels))
	height = math.ceil(num_pixels / width)
	# Pad pixels to fill the image
	while len(pixels) < width * height:
		pixels.append((0, 0, 0, 255))
	make_png(width, height, pixels, output_file)
	print(f"Wrote {output_file} ({width}x{height} pixels)")

if __name__ == "__main__":
	main()
