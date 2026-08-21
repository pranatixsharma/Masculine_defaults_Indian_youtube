import os
import pandas as pd

CSV_PATH = "data/videos_raw.csv"
AUDIO_DIR = "audio"  # adjust to your actual audio folder path

# channels you just fixed - so you can see their status called out clearly
NEWLY_ADDED_CHANNELS = [
    "NehaNagar", "Michu", "RiaSehgal", "PrakritiSingh",
    "FitTuberHindi", "WomenAndWorkCareer", "FitBharat", "GunjanShouts",
]

df = pd.read_csv(CSV_PATH)
print(f"Checking audio for {len(df)} videos across {df['channel_title'].nunique()} channels\n")

# collect every filename already on disk, across all subfolders
existing_files = set()
for root, dirs, files in os.walk(AUDIO_DIR):
    for f in files:
        existing_files.add(f)

def has_audio(video_id):
    # matches on video_id being present anywhere in the filename,
    # so it works regardless of your exact naming convention (channel__videoID.ext)
    return any(video_id in f for f in existing_files)

df["audio_downloaded"] = df["video_id"].apply(has_audio)

found_count = df["audio_downloaded"].sum()
missing_count = len(df) - found_count
print(f"Found audio:   {found_count}/{len(df)}")
print(f"Missing audio: {missing_count}/{len(df)}\n")

# breakdown by channel
summary = df.groupby("channel_title")["audio_downloaded"].agg(
    total="count", downloaded="sum"
)
summary["missing"] = summary["total"] - summary["downloaded"]
summary = summary.sort_values("missing", ascending=False)

print("Per-channel breakdown (sorted by most missing first):")
print(summary.to_string())

# highlight specifically the channels you just added
print("\n--- Newly added channels (the ones you just fixed) ---")
newly_added_summary = summary[summary.index.isin(NEWLY_ADDED_CHANNELS)]
if not newly_added_summary.empty:
    print(newly_added_summary.to_string())
else:
    print("None of these channel names matched what's in the CSV - check spelling/mapping.")

# save the full missing list so you can feed it straight into your downloader
missing_df = df[~df["audio_downloaded"]][["video_id", "title", "channel_title"]]
missing_df.to_csv("missing_audio.csv", index=False)
print(f"\nFull list of {len(missing_df)} missing videos saved to missing_audio.csv")