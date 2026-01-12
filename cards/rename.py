import os
import re

# Folder containing your card images
FOLDER_PATH = "cards"   # change if needed

# Regex: finds _0X where X is 1–9
pattern = re.compile(r'_0([1-9])')

for filename in os.listdir(FOLDER_PATH):
    old_path = os.path.join(FOLDER_PATH, filename)

    # Skip non-files
    if not os.path.isfile(old_path):
        continue

    # Replace _07 -> _7, _02 -> _2, etc
    new_filename = pattern.sub(r'_\1', filename)

    if new_filename != filename:
        new_path = os.path.join(FOLDER_PATH, new_filename)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_filename}")

print("Done!")
