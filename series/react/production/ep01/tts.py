#!/usr/bin/env python3
"""Generate TTS for React ep01: Your First Component"""
import soundfile as sf
import json
import numpy as np
import types
from kokoro_onnx import Kokoro, MAX_PHONEME_LENGTH, SAMPLE_RATE

kokoro = Kokoro(
    '/Users/claude/runthedocs/kokoro/onnx/model.onnx',
    '/Users/claude/runthedocs/kokoro/voices.npz'
)

def patched_create_audio(self, phonemes, voice, speed):
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

INTRO_SILENCE = 2.0
GAP = 0.4

sentences = [
    "React is built on components. Let's learn what they are.",
    "A component is a reusable piece of the user interface.",
    "It can be as small as a button, or as large as an entire page.",
    "In React, components are just JavaScript functions that return markup.",
    "Here's a button component. It's a function called MyButton that returns a button element.",
    "To use your component, you reference it like any other JSX element.",
    "Just make sure to capitalize the first letter. That tells React it's a component, not an HTML tag.",
    "You can use the same component multiple times, and you can nest components inside other components to build complex user interfaces.",
    "Components are the building blocks of every React app.",
    "Start with functions, and you can build anything.",
    "Next episode: learn about Props to pass data to your components.",
]

print(f"Generating {len(sentences)} sentences...")
segments = []
all_audio = []

intro_samples = int(INTRO_SILENCE * SAMPLE_RATE)
all_audio.append(np.zeros(intro_samples, dtype=np.float32))
current_time = INTRO_SILENCE

for i, sentence in enumerate(sentences):
    print(f"  [{i+1}/{len(sentences)}] {sentence[:70]}...")
    audio, sr = kokoro.create(sentence, voice='bm_george', speed=1.0, lang='en-us')
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
    if i < len(sentences) - 1:
        gap_samples = int(GAP * SAMPLE_RATE)
        all_audio.append(np.zeros(gap_samples, dtype=np.float32))
        current_time += GAP

final_audio = np.concatenate(all_audio)
output_path = 'voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)
print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

timing_path = 'timing.json'
with open(timing_path, 'w') as f:
    json.dump({
        "segments": segments,
        "total_voice_duration": round(current_time, 4),
        "total_duration": round(current_time + 4.0, 4),
        "total_frames_30fps": int(np.ceil((current_time + 4.0) * 30)),
    }, f, indent=2)
print(f"Saved timing: {timing_path}")
