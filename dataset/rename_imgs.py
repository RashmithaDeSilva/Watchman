import os
from PIL import Image

# Path to your folder
folder_path = 'imgs'

# Get list of all files in the folder
files = os.listdir(folder_path)

# Filter to only keep image files (optional, but safer)
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
images = [f for f in files if f.lower().endswith(image_extensions)]

# Sort the images (optional, for consistent order)
images.sort()

# Loop through images and rename
for idx, filename in enumerate(images, start=1):
    old_path = os.path.join(folder_path, filename)
    new_filename = f"{idx}.png"
    new_path = os.path.join(folder_path, new_filename)
    
    # Open image and save it as PNG
    with Image.open(old_path) as img:
        img.save(new_path, "PNG")
    
    # Optionally, remove the old file if it was not already PNG
    if not filename.lower().endswith('.png'):
        os.remove(old_path)

print("Renaming and conversion complete.")