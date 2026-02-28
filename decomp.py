# Simple PNG-to-File Decompressor
#
# This script reverses the process of comp.py:
# 1. Reads a PNG image created by comp.py
# 2. Extracts RGBA 4-bit segments from each pixel
# 3. Reconstructs the original bytes and writes them to an output file
#
# Only Python 3 standard libraries are used.
#
# Usage: python3 decomp.py <input_image.png> <output_file>

import sys
import struct
import zlib

def read_png_rgba_pixels(png_path):
	"""Read RGBA pixels from a PNG file (no external libraries)."""
	with open(png_path, 'rb') as f:
		data = f.read()
	# Check PNG signature
	if data[:8] != b'\x89PNG\r\n\x1a\n':
		raise ValueError("Not a valid PNG file")
	pos = 8
	width = height = None
	idat_data = b''
	while pos < len(data):
		chunk_len = struct.unpack('>I', data[pos:pos+4])[0]
		chunk_type = data[pos+4:pos+8]
		chunk_data = data[pos+8:pos+8+chunk_len]
		# chunk_crc = data[pos+8+chunk_len:pos+12+chunk_len]  # Not used
		if chunk_type == b'IHDR':
			width, height, bit_depth, color_type, _, _, _ = struct.unpack('>IIBBBBB', chunk_data)
			if bit_depth != 8 or color_type != 6:
				raise ValueError("Only 8-bit RGBA PNGs supported")
		elif chunk_type == b'IDAT':
			idat_data += chunk_data
		elif chunk_type == b'IEND':
			break
		pos += 8 + chunk_len + 4
	# Decompress image data
	raw = zlib.decompress(idat_data)
	# Parse scanlines
	pixels = []
	stride = width * 4
	i = 0
	for y in range(height):
		filter_type = raw[i]
		if filter_type != 0:
			raise ValueError("Only filter type 0 supported")
		i += 1
		row = raw[i:i+stride]
		for x in range(width):
			px = row[x*4:(x+1)*4]
			pixels.append(tuple(px))
		i += stride
	return pixels

def rgba_pixels_to_4bit_segments(pixels):
	"""Extract 4-bit segments from RGBA pixels (reverse of comp.py)."""
	segments = []
	for px in pixels:
		for c in px:
			# Reverse scaling: 8-bit (0-255) to 4-bit (0-15)
			seg = c // 17
			segments.append(seg)
	return segments

def segments_to_bytes(segments):
	"""Combine 4-bit segments into bytes (2 segments per byte)."""
	out = bytearray()
	for i in range(0, len(segments)-1, 2):
		byte = ((segments[i] & 0xF) << 4) | (segments[i+1] & 0xF)
		out.append(byte)
	return out

def main():
	if len(sys.argv) != 3:
		print("Usage: python3 decomp.py <input_image.png> <output_file>")
		sys.exit(1)
	input_png = sys.argv[1]
	output_file = sys.argv[2]
	pixels = read_png_rgba_pixels(input_png)
	segments = rgba_pixels_to_4bit_segments(pixels)
	data = segments_to_bytes(segments)
	# Remove trailing zero padding (if any)
	# Note: This will not recover the exact original file size if the original file ended with 0x00 bytes.
	# If exact size is needed, store the original file size in the PNG metadata in comp.py.
	with open(output_file, 'wb') as f:
		f.write(data.rstrip(b'\x00'))
	print(f"Wrote {output_file} ({len(data.rstrip(b'\x00'))} bytes)")

if __name__ == "__main__":
	main()
