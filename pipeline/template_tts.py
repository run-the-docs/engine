#!/usr/bin/env python3
"""
Template TTS script for Run the Docs episodes.

USAGE:
1. Copy this file to series/<name>/production/ep<NN>/tts.py
2. Edit the `sentences` list with your episode narration
3. Run: python3 tts.py
4. Outputs: voice.wav + timing.json

timing.json will contain:
- total_voice_duration: seconds (voice only, no silence)
- total_duration: seconds (voice + 4s outro buffer)
- total_frames_30fps: frame count for rendering
- segments: array of {start, end, duration, text}
"""

import soundfile as sf
import json
import numpy as np
import types
from kokoro_onnx import Kokoro, MAX_PHONEME_LENGTH, SAMPLE_RATE

kokoro = Kokoro('/Users/claude/runthedocs/kokoro/onnx/model.onnx', 
                '/Users/claude/runthedocs/kokoro/voices.npz')

def patched_create_audio(self, phonemes, voice, speed):
    """Patch to handle Kokoro audio generation"""
    phonemes = phonemes[:MAX_PHONEME_LENGTH]
    tokens = np.array(self.tokenizer.tokenize(phonemes), dtype=np.int64)
    style = voice[len(tokens)]
    tokens_arr = [[0, *tokens, 0]]
    inputs = {
        'input_ids': tokens_arr,
        'style': np.array(style, dtype=np.float32).reshape(1, -1),
        'speed': np.array([speed], dtype=np.float32),
    }
    audio = self.sess.run(None, inputs)[0]
    return audio, SAMPLE_RATE

kokoro._create_audio = types.MethodType(patched_create_audio, kokoro)

# === EDIT THESE ===
INTRO_SILENCE = 2.0  # Silence before first sentence
GAP = 0.38           # Gap between sentences
VOICE = 'bm_george'  # Kokoro voice (don't change)
SPEED = 1.0          # Narration speed (1.0 = normal)
OUTRO_BUFFER = 4.0   # Silence after last sentence

sentences = [
    # EDIT: Replace with your episode narration
    "This is a template episode.",
    "Replace these sentences with your narration.",
    "Each string becomes one TTS segment.",
]
# === END EDIT ===

print(f"Generating {len(sentences)} sentences with Kokoro ({VOICE})...")
segments = []
all_audio = []

# Add intro silence
intro_samples = int(INTRO_SILENCE * SAMPLE_RATE)
all_audio.append(np.zeros(intro_samples, dtype=np.float32))
current_time = INTRO_SILENCE

# Generate each sentence
for i, sentence in enumerate(sentences):
    print(f"  [{i+1}/{len(sentences)}] {sentence[:70]}...")
    audio, sr = kokoro.create(sentence, voice=VOICE, speed=SPEED, lang='en-us')
    audio_flat = audio.flatten()
    start = current_time
    duration = len(audio_flat) / sr
    end = start + duration
    
    segments.append({
        "index": i,
        "text": sentence,
        "start": round(start, 4),
        "end": round(end, 4),
        "duration": round(duration, 4)
    })
    
    all_audio.append(audio_flat)
    current_time = end
    
    # Add gap between sentences (but not after last)
    if i < len(sentences) - 1:
        gap_samples = int(GAP * SAMPLE_RATE)
        all_audio.append(np.zeros(gap_samples, dtype=np.float32))
        current_time += GAP

# Concatenate all audio
final_audio = np.concatenate(all_audio)
output_path = 'voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)

print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

# Calculate total duration (voice + outro buffer)
total_duration = current_time + OUTRO_BUFFER
total_frames = int(np.ceil(total_duration * 30))  # 30fps

# Write timing.json
timing_path = 'timing.json'
with open(timing_path, 'w') as f:
    json.dump({
        "segments": segments,
        "total_voice_duration": round(current_time, 4),
        "total_duration": round(total_duration, 4),
        "total_frames_30fps": total_frames,
    }, f, indent=2)

print(f"Saved timing: {timing_path}")
print(f"Total frames at 30fps: {total_frames}")
print(f"\nTiming summary:")
for seg in segments:
    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text'][:60]}")
print(f"\nOutro buffer: {OUTRO_BUFFER}s")
print(f"Final duration: {total_duration:.2f}s ({total_frames} frames @ 30fps)")
