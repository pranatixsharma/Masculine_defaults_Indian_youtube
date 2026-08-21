# copy_sample_audios.py
# Copies 1 audio file from each channel into a new sample folder

import os
import shutil
import pandas as pd

AUDIO_DIR   = r"D:\hindi_discourse_study\audio"
SAMPLE_DIR  = r"D:\hindi_discourse_study\audio_samples"
CSV_FILE    = "data/videos_raw.csv"

os.makedirs(SAMPLE_DIR, exist_ok=True)

df = pd.read_csv(CSV_FILE)

# get all unique channels
channels = df["channel_title"].unique()
print(f"Total channels: {len(channels)}")

copied   = 0
missing  = 0

for community in os.listdir(AUDIO_DIR):
    folder = os.path.join(AUDIO_DIR, community)
    if not os.path.isdir(folder):
        continue

    # track which channels we already copied from this community
    copied_channels = set()

    for fname in os.listdir(folder):
        if not fname.endswith(".mp3"):
            continue
        if "__" not in fname:
            continue

        # extract channel name from filename
        channel = fname.split("__")[0]

        # copy only first file per channel
        if channel not in copied_channels:
            src = os.path.join(folder, fname)
            dst = os.path.join(SAMPLE_DIR, fname)
            shutil.copy2(src, dst)
            copied_channels.add(channel)
            copied += 1
            print(f"Copied: {fname}")

print(f"\n{'='*45}")
print(f"DONE")
print(f"{'='*45}")
print(f"Copied  : {copied} files")
print(f"Saved in: {SAMPLE_DIR}")
