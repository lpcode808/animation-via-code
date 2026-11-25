#!/usr/bin/env bash
# Joins frames/ and audio.wav into out.mp4 that plays everywhere.
# Loudness ~-15 LUFS with a true-peak ceiling; AAC raises peaks, so measure the result.
set -euo pipefail
FPS="${1:-30}"
ffmpeg -y -loglevel error -framerate "$FPS" -i frames/%05d.jpg -i audio.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart \
  -af "loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.7:level=false" -c:a aac -b:a 192k -ar 48000 out.mp4
echo "wrote out.mp4"
# Check the length: it must equal the frame count divided by fps, within one frame.
N=$(ls frames | wc -l)
python3 - "$N" "$FPS" "$(ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4)" <<'PY'
import sys
n, fps, got = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
want = n / fps
assert abs(got - want) <= 1.5 / fps, f"out.mp4 is {got:.3f} s, expected {want:.3f} s"
print(f"length ok: {got:.3f} s")
PY
# Check the real peak after encoding:
ffmpeg -hide_banner -i out.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A1 "True peak" | tail -1
