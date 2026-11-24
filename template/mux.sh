#!/usr/bin/env bash
# Joins frames/ and audio.wav into out.mp4 that plays everywhere.
# Loudness ~-15 LUFS with a true-peak ceiling; AAC raises peaks, so measure the result.
set -euo pipefail
FPS="${1:-30}"
ffmpeg -y -loglevel error -framerate "$FPS" -i frames/%05d.jpg -i audio.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart \
  -af "loudnorm=I=-15:TP=-2:LRA=11,alimiter=limit=0.7:level=false" -c:a aac -b:a 192k -ar 48000 -shortest out.mp4
echo "wrote out.mp4"
# Check the real peak after encoding:
ffmpeg -hide_banner -i out.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A1 "True peak" | tail -1
