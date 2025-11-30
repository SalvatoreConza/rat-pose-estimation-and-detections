import os
import subprocess

# Sostituisci questo percorso con la tua cartella principale
root_dir = r"D:\20250312 - Dyskineisa - Mike Rat no 3 - 20mgLD 8mgB"

for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.lower().endswith('.mkv'):
            mkv_path = os.path.join(subdir, file)
            mp4_name = os.path.splitext(file)[0] + ".mp4"
            mp4_path = os.path.join(subdir, mp4_name)
            cmd = [
                "ffmpeg",
                "-fflags", "+genpts",
                "-i", mkv_path,
                "-c:v", "copy",
                "-c:a","copy", "-avoid_negative_ts", "make_zero",
                mp4_path
            ]
            print(f"Converting: {mkv_path} -> {mp4_path}")
            subprocess.run(cmd, check=True)
            os.remove(mkv_path)
            print(f"Removed: {mkv_path}")