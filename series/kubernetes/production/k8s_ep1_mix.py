#!/usr/bin/env python3
"""Mix TTS voice with SFX for K8s Ep1"""
import numpy as np
import soundfile as sf
import json

SR = 24000  # kokoro SR
SR_SFX = 44100

def load_wav(path, target_sr=None):
    audio, sr = sf.read(path, dtype='float32')
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if target_sr and sr != target_sr:
        # Simple resampling
        ratio = target_sr / sr
        n_samples = int(len(audio) * ratio)
        audio = np.interp(
            np.linspace(0, len(audio)-1, n_samples),
            np.arange(len(audio)),
            audio
        ).astype(np.float32)
    return audio

# Load timing
with open('/tmp/k8s_ep1_timing.json') as f:
    timing_data = json.load(f)
total_dur = timing_data['total_voice_duration']

# Load voice (at 24000 Hz)
voice, voice_sr = sf.read('/tmp/k8s_ep1_voice.wav', dtype='float32')
if voice.ndim > 1:
    voice = voice.mean(axis=1)
print(f"Voice: {len(voice)/voice_sr:.2f}s at {voice_sr}Hz")

# Add 4s of silence at the end for outro fade
outro_silence = int(4.0 * voice_sr)
voice = np.concatenate([voice, np.zeros(outro_silence, dtype=np.float32)])
total_samples = len(voice)
total_dur_final = total_samples / voice_sr
print(f"Total with outro: {total_dur_final:.2f}s")

# Create mix buffer at voice SR
mix = voice.copy()

def mix_sfx(sfx_path, insert_time_s, volume=0.5, target_sr=None):
    """Mix an SFX into the buffer at given time"""
    sfx, sr = sf.read(sfx_path, dtype='float32')
    if sfx.ndim > 1:
        sfx = sfx.mean(axis=1)
    if sr != voice_sr:
        ratio = voice_sr / sr
        n = int(len(sfx) * ratio)
        sfx = np.interp(
            np.linspace(0, len(sfx)-1, n),
            np.arange(len(sfx)),
            sfx
        ).astype(np.float32)
    start_sample = int(insert_time_s * voice_sr)
    end_sample = min(start_sample + len(sfx), total_samples)
    sfx_len = end_sample - start_sample
    mix[start_sample:end_sample] += sfx[:sfx_len] * volume
    print(f"  Mixed {sfx_path} at {insert_time_s:.2f}s (vol={volume})")

# Add SFX at appropriate times
print("\nMixing SFX...")

# Alert beep at scene 1 hook (just before "container crashed")
mix_sfx('/tmp/k8s_ep1_alert_beep.wav', 1.7, volume=0.4)
mix_sfx('/tmp/k8s_ep1_crash_sound.wav', 2.3, volume=0.35)

# Whoosh scene transitions
scene_transitions = [9.0, 23.6, 38.6, 58.5, 71.0, 83.9]
for st in scene_transitions:
    mix_sfx('/tmp/k8s_ep1_whoosh.wav', st, volume=0.35)

# Pop for each feature row (scene 4)
feature_pops = [40.7, 44.8, 47.5, 50.9, 54.7]
for pt in feature_pops:
    mix_sfx('/tmp/k8s_ep1_pop.wav', pt, volume=0.3)

# Pods fix chime at scene 6 payoff
mix_sfx('/tmp/k8s_ep1_pods_fix_chime.wav', 73.5, volume=0.45)

# Normalize to avoid clipping
peak = np.max(np.abs(mix))
if peak > 0.95:
    mix = mix * (0.95 / peak)
    print(f"Normalized (peak was {peak:.3f})")

# Save final mixed audio
output_path = '/tmp/k8s_ep1_mixed.wav'
sf.write(output_path, mix, voice_sr)
print(f"\nSaved: {output_path} ({total_dur_final:.2f}s)")

# Save updated timing with total duration for render
with open('/tmp/k8s_ep1_timing.json', 'w') as f:
    json.dump({
        "segments": timing_data["segments"],
        "total_voice_duration": timing_data["total_voice_duration"],
        "total_duration": round(total_dur_final, 2),
        "total_frames_30fps": int(total_dur_final * 30) + 30,
    }, f, indent=2)
print("Updated timing JSON with total_duration and frame count")
