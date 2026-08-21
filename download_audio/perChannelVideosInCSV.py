import pandas as pd

CSV_PATH = "data/videos_raw.csv"

df = pd.read_csv(CSV_PATH)

counts = df["channel_title"].value_counts()

print(f"Total videos: {len(df)}")
print(f"Total unique channels: {df['channel_title'].nunique()}\n")

print("Videos per channel (sorted, highest first):")
print(counts.to_string())

# save it to a file too, so you don't have to re-run this every time you want to check
counts.to_csv("videos_per_channel.csv", header=["video_count"])
print("\nSaved to videos_per_channel.csv")
