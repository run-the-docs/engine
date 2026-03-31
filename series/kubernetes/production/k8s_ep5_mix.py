#!/usr/bin/env python3
"""Mix TTS voice + SFX + background music for K8s Ep5: Services"""
import numpy as np
import soundfile as sf
import json
import os

SR = 24000  # kokoro output SR

def load_wav(path, target_sr=SR):
    audio, sr = sf.read(path, dtype='float32')
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != target_sr:
        ratio = target_sr / sr
        n_samples = int(len(audio) * ratio)
        audio = np.interp(
            np.linspace(0, len(audio)-1, n_samples),
            np.arange(len(audio)),
            audio
        ).astype(np.float32)
    return audio

# Load timing
with open('/tmp/k8s_ep5_timing.json') as f:
    timing_data = json.load(f)
total_dur = timing_data['total_duration']

# Load voice
voice = load_wav('/tmp/k8s_ep5_voice.wav', SR)
print(f"Voice: {len(voice)/SR:.2f}s at {SR}Hz")

# Pad to total_duration + 2s fade
target_samples = int((total_dur + 2.0) * SR)
if len(voice) < target_samples:
    voice = np.concatenate([voice, np.zeros(target_samples - len(voice), dtype=np.float32)])

mix = voice.copy()
total_samples = len(mix)

def mix_sfx(sfx_path, insert_time_s, volume=0.5):
    """Mix SFX at given time"""
    if not os.path.exists(sfx_path):
        print(f"  [SKIP] {sfx_path} not found")
        return
    sfx = load_wav(sfx_path, SR)
    start = int(insert_time_s * SR)
    end = min(start + len(sfx), total_samples)
    n = end - start
    mix[start:end] += sfx[:n] * volume
    print(f"  Mixed {os.path.basename(sfx_path)} at t={insert_time_s:.1f}s vol={volume}")

# Sound design
print("Mixing SFX...")
mix_sfx('/tmp/k8s_ep5_impact_thud.wav',     insert_time_s=2.0,   volume=0.55)  # hook reveal
mix_sfx('/tmp/k8s_ep5_ascending_chime.wav', insert_time_s=68.0,  volume=0.45)  # payoff (One Service. Many Pods.)

# Background music at 2.5%
for bgm_path in ['/tmp/eco-technology.mp3', '/tmp/rewe-bg-music.mp3']:
    if os.path.exists(bgm_path):
        print(f"Adding BG music: {bgm_path}")
        bgm = load_wav(bgm_path, SR)
        # Loop if needed
        if len(bgm) < total_samples:
            reps = int(np.ceil(total_samples / len(bgm)))
            bgm = np.tile(bgm, reps)
        bgm = bgm[:total_samples]
        # Fade out last 3s
        fade_len = int(3.0 * SR)
        bgm[-fade_len:] *= np.linspace(1, 0, fade_len)
        mix += bgm * 0.025
        break

# Normalize
peak = np.max(np.abs(mix))
if peak > 0.95:
    mix = mix * (0.95 / peak)
    print(f"Normalized (peak was {peak:.3f})")

# Convert to 44100 for output
mix_44 = np.interp(
    np.linspace(0, len(mix)-1, int(len(mix) * 44100/SR)),
    np.arange(len(mix)),
    mix
).astype(np.float32)

output_path = '/tmp/k8s_ep5_mixed.wav'
sf.write(output_path, mix_44, 44100)
print(f"\nSaved: {output_path} ({len(mix_44)/44100:.2f}s at 44100Hz)")
