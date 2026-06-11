import os
import mutagen.mp3

for i in range(1, 12):
    filename = f"slide_{i}.mp3"
    filepath = os.path.join('video_project/app/assets_v2', filename)
    if os.path.exists(filepath):
        audio = mutagen.mp3.MP3(filepath)
        print(f"{filename}: {audio.info.length:.2f}s")
    else:
        print(f"{filename} does not exist yet.")
