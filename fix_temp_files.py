# fix_temp_files.py

import os
import subprocess
import pandas as pd

AUDIO_DIR   = r"D:\hindi_discourse_study\audio"
CSV_FILE    = "data/videos_raw.csv"
FFMPEG      = r"C:\Users\roshn\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"

# build lookup: video_id → channel_title
df = pd.read_csv(CSV_FILE)
lookup = {}
for _, row in df.iterrows():
    vid     = str(row["video_id"]).strip()
    channel = str(row["channel_title"]).strip().replace(" ", "_")
    lookup[vid] = channel

deleted  = 0
fixed    = 0
unknown  = 0

for community in os.listdir(AUDIO_DIR):
    folder = os.path.join(AUDIO_DIR, community)
    if not os.path.isdir(folder):
        continue

    for fname in os.listdir(folder):
        old_path = os.path.join(folder, fname)

        # ── Case 1: __temp__videoID.mp3 ───────────────────────
        # these are stuck temp files — trim and rename properly
        if fname.startswith("__temp__") and fname.endswith(".mp3"):
            video_id = fname.replace("__temp__", "").replace(".mp3", "")

            if video_id in lookup:
                channel      = lookup[video_id]
                final_name   = f"{channel}__{video_id}.mp3"
                final_path   = os.path.join(folder, final_name)

                # trim to exactly 600 seconds and save as final file
                try:
                    subprocess.run([
                        FFMPEG, "-y",
                        "-i", old_path,
                        "-t", "600",
                        "-c", "copy",
                        "-loglevel", "error",
                        final_path
                    ], check=True, timeout=60, capture_output=True)

                    os.remove(old_path)
                    print(f"Fixed temp: {fname} → {final_name}")
                    fixed += 1

                except Exception as e:
                    # if trim fails, file is likely corrupted — delete it
                    print(f"Corrupted temp, deleting: {fname} — {e}")
                    try:
                        os.remove(old_path)
                        deleted += 1
                    except:
                        pass
            else:
                # video_id not in CSV — just delete it
                print(f"Unknown temp, deleting: {fname}")
                try:
                    os.remove(old_path)
                    deleted += 1
                except:
                    pass

        # ── Case 2: __temp__videoID.m4a or .webm (not mp3) ────
        elif fname.startswith("__temp__"):
            print(f"Deleting non-mp3 temp: {fname}")
            try:
                os.remove(old_path)
                deleted += 1
            except:
                pass

        # ── Case 3: .part files (incomplete downloads) ─────────
        elif fname.endswith(".part"):
            print(f"Deleting incomplete .part: {fname}")
            try:
                os.remove(old_path)
                deleted += 1
            except:
                pass

        # ── Case 4: plain videoID.mp3 (no channel name) ───────
        elif "__" not in fname and fname.endswith(".mp3"):
            video_id = fname.replace(".mp3", "")
            if video_id in lookup:
                channel    = lookup[video_id]
                new_name   = f"{channel}__{video_id}.mp3"
                new_path   = os.path.join(folder, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {fname} → {new_name}")
                fixed += 1
            else:
                print(f"Unknown video_id, deleting: {fname}")
                try:
                    os.remove(old_path)
                    deleted += 1
                except:
                    pass

print(f"\n{'='*45}")
print(f"CLEANUP COMPLETE")
print(f"{'='*45}")
print(f"Fixed/renamed : {fixed}")
print(f"Deleted       : {deleted}")
print(f"Unknown       : {unknown}")