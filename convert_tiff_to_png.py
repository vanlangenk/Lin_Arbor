from PIL import Image

Image.new('RGB', (100, 100), 'green').save(r"C:\Users\kenne\Lin_Arbor\docs\test_output.png")
import os

tiff_path = r"C:\Users\kenne\Lin_Arbor\data\Linwood-Arboretum-4-13-2025-orthophoto.tif"
png_path = r"C:\Users\kenne\Lin_Arbor\docs\test_output.png"

print(f"Trying to open: {tiff_path}")
if not os.path.exists(tiff_path):
    print("ERROR: TIFF file not found.")
    exit()

try:
    img = Image.open(tiff_path)
    print(f"Opened file. Mode: {img.mode}, Size: {img.size}, Format: {img.format}")

    # Force RGB conversion before saving
    img = img.convert("RGB")

    img.save(png_path, format='PNG')
    print(f"✅ Saved PNG to: {png_path}")
except Exception as e:
    print(f"❌ FAILED to open/save image: {e}")
