#!/usr/bin/env bash
# 12 stills in a 4x3 grid, for a quick look and for the review pass.
set -euo pipefail
N=$(ls frames | wc -l); STEP=$(( N / 12 )); [ "$STEP" -ge 1 ] || STEP=1
ffmpeg -y -loglevel error -framerate 30 -i frames/%05d.jpg \
  -vf "select='not(mod(n\,$STEP))',scale=480:-1,tile=4x3" -frames:v 1 contact.jpg
echo "wrote contact.jpg"
