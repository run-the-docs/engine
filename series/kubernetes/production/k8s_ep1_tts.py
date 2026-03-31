#!/usr/bin/env python3
"""Generate TTS for Kubernetes Ep1: What is Kubernetes?"""
import soundfile as sf
import json
import numpy as np
import types
from kokoro_onnx import Kokoro, MAX_PHONEME_LENGTH, SAMPLE_RATE

kokoro = Kokoro('/tmp/kokoro/onnx/model.onnx', '/tmp/kokoro/voices.npz')

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
GAP = 0.38

# Script sentences — punchy dev voice, 65-75s total
sentences = [
    # HOOK (starts ~2s)
    "Your container just crashed. Again. At 3am. You woke up to fix it.",
    "There's a better way.",
    # CONTEXT
    "Three eras. Physical servers — resource conflicts, expensive. Virtual machines — better isolation, but heavyweight. Containers — lightweight, portable. But at scale?",
    "At scale, you need something to manage them.",
    # WHAT IS IT
    "That something is Kubernetes. Open-source container orchestration from Google, released in 2014.",
    "Named from the Greek word for helmsman. Abbreviated K-8-s — eight letters between K and s.",
    # WHAT IT DOES
    "Five things that matter.",
    "Self-healing: restarts crashed containers automatically.",
    "Scaling: up or down, on demand.",
    "Rollouts: zero-downtime deployments.",
    "Load balancing: traffic distribution built in.",
    "Secrets: passwords and config, managed safely.",
    # WHAT IT'S NOT
    "What Kubernetes is not. It's not a platform as a service. It doesn't build your code. It doesn't include databases or message buses.",
    "It's building blocks. You choose the rest.",
    # PAYOFF
    "You describe the desired state. Three pods running. Kubernetes figures out how to get there — and keeps it there.",
    "A container crashes? K8s restarts it. No 3am wake-up.",
    # OUTRO
    "Run the Docs. Kubernetes. Episode one of thirteen.",
]

print(f"Generating {len(sentences)} sentences...")

segments = []
all_audio = []

intro_samples = int(INTRO_SILENCE * SAMPLE_RATE)
all_audio.append(np.zeros(intro_samples, dtype=np.float32))
current_time = INTRO_SILENCE

for i, sentence in enumerate(sentences):
    print(f"  [{i+1}/{len(sentences)}] {sentence[:60]}...")
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
output_path = '/tmp/k8s_ep1_voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)
print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

timing_path = '/tmp/k8s_ep1_timing.json'
with open(timing_path, 'w') as f:
    json.dump({"segments": segments, "total_voice_duration": round(current_time, 4)}, f, indent=2)
print(f"Saved timing: {timing_path}")
print("\nTiming summary:")
for seg in segments:
    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text'][:70]}")
