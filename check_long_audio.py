import os
import subprocess
import json

AUDIO_DIR = r"D:\hindi_discourse_study\audio"
FFPROBE = r"C:\Users\roshn\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffprobe.exe"

def get_duration(path):
    try:
        result = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries", "format=duration",
             "-of", "json", path],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception as e:
        print(f"  ERROR checking {path}: {e}")
        return None

long_files = []
total_checked = 0

print("Starting scan...")
print(f"Audio dir: {AUDIO_DIR}\n")

for community in os.listdir(AUDIO_DIR):
    folder = os.path.join(AUDIO_DIR, community)
    if not os.path.isdir(folder):
        continue

    print(f"Scanning: {community}")
    files_in_folder = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    print(f"  Found {len(files_in_folder)} mp3 files")

    for fname in files_in_folder:
        path = os.path.join(folder, fname)
        dur = get_duration(path)
        total_checked += 1

        if dur and dur > 605:
            long_files.append((path, dur))

        if total_checked % 100 == 0:
            print(f"  Checked {total_checked} files so far...")

print(f"\n{'='*50}")
print(f"SCAN COMPLETE")
print(f"{'='*50}")
print(f"Total checked: {total_checked}")
print(f"Files longer than 10 min: {len(long_files)}\n")

for path, dur in long_files[:20]:
    print(f"  {dur:.0f}s — {path}")