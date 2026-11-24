"""Writes audio.wav: a short synth pad on a bar grid plus sound effects placed
from cues.json (written by render.mjs). No samples, just numpy."""
import json, wave
import numpy as np

SR, DUR = 48000, 6.0                    # keep in step with DURATION in scene.html
t = np.arange(int(SR * DUR)) / SR
mix_music = np.zeros_like(t)
mix_fx = np.zeros_like(t)
rng = np.random.default_rng(7)          # seeded: same file every run

def env(n, attack=0.01, release=0.05):
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.linspace(1, 0, r)      # always fade out: no clicks at note ends
    return e

# Music: 120 bpm, so one bar = 2 s. (The captions change at 1.3 s and 2.6 s to follow the physics, not the bars.)
chords = [[220.0, 277.18, 329.63], [196.0, 246.94, 293.66], [174.61, 220.0, 261.63]]
for bar, chord in enumerate(chords):
    s, n = int(bar * 2 * SR), int(2 * SR)
    seg = np.zeros(n)
    for f in chord:
        for detune in (-0.3, 0.0, 0.3):  # detuned stack, random phases: no pulsing
            ph = rng.uniform(0, 2 * np.pi)
            seg += np.sin(2 * np.pi * (f + detune) * t[:n] + ph)
    mix_music[s:s + n] += 0.03 * seg * env(n, 0.3, 0.4)

# Effects from the picture's cues.
for c in json.load(open('cues.json')):
    s = int(c['t'] * SR)
    if c['type'] == 'bounce':
        n = int(0.12 * SR); x = t[:n]
        thump = np.sin(2 * np.pi * 90 * x) * np.exp(-x * 40)
        crack = rng.standard_normal(n) * np.exp(-x * 120) * 0.3   # small bright layer for phone speakers
        sig = (thump + crack) * env(n, 0.001, 0.02)
    else:  # tick
        n = int(0.05 * SR); x = t[:n]
        sig = 0.3 * np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 90) * env(n, 0.001, 0.01)
    end = min(len(t), s + n)
    mix_fx[s:end] += 0.6 * sig[:end - s]

# Duck music ~6 dB wherever effects are playing.
fx_env = np.convolve(np.abs(mix_fx), np.ones(2400) / 2400, mode='same')
duck = 1 - 0.5 * np.clip(fx_env / (fx_env.max() + 1e-9) * 4, 0, 1)
out = mix_music * duck + mix_fx
out *= 0.7 / np.max(np.abs(out))        # leave headroom; mux.sh normalizes and limits

pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote audio.wav')
