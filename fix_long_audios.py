import os
import subprocess

AUDIO_DIR = r"D:\hindi_discourse_study\audio"
FFMPEG_PATH = r"C:\Users\roshn\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"
FFMPEG = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
FFPROBE = os.path.join(FFMPEG_PATH, "ffprobe.exe")

import json

def get_duration(path):
    try:
        result = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except:
        return None

fixed = 0
failed = 0

for community in os.listdir(AUDIO_DIR):
    folder = os.path.join(AUDIO_DIR, community)
    if not os.path.isdir(folder):
        continue
    for fname in os.listdir(folder):
        if not fname.endswith(".mp3"):
            continue
        path = os.path.join(folder, fname)
        dur = get_duration(path)

        if dur and dur > 605:
            temp_path = path + ".trimmed.mp3"
            try:
                subprocess.run(
                    [FFMPEG, "-y", "-i", path, "-t", "600",
                     "-c", "copy", "-loglevel", "error", temp_path],
                    check=True, timeout=60, capture_output=True
                )
                os.remove(path)
                os.rename(temp_path, path)
                fixed += 1
                print(f"Fixed: {fname} ({dur:.0f}s -> 600s)")
            except Exception as e:
                failed += 1
                print(f"Failed: {fname} — {e}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)

print(f"\nFixed: {fixed}")
print(f"Failed: {failed}")