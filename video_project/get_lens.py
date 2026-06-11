import os
import mutagen.mp3

for f in sorted(os.listdir('app/assets')):
    if f.endswith('.mp3'):
        audio = mutagen.mp3.MP3(os.path.join('app/assets', f))
        print(f"{f}: {audio.info.length:.2f}s")
