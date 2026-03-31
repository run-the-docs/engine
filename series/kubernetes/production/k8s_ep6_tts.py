#!/usr/bin/env python3
"""Generate TTS for Kubernetes Ep6: ConfigMaps"""
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

sentences = [
    # HOOK (0-8s)
    "Same code.",
    "Different config per environment.",
    "ConfigMaps make that work.",
    # THE PROBLEM (8-22s)
    "Picture this: DATABASE_HOST equals localhost, hardcoded in your app.",
    "Works in dev. Breaks in production.",
    "The fix seems obvious: bake config into the image.",
    "But then every environment change means a rebuild.",
    "ConfigMap breaks that cycle.",
    "It stores configuration outside your container image as key-value pairs.",
    # THREE WAYS (22-38s)
    "Once you have a ConfigMap, pods consume it three ways.",
    "First: environment variables. Inject values directly into the container.",
    "Second: command-line arguments. Pass config values as flags at startup.",
    "Third: files mounted in a volume. Drop a whole settings file at a path like slash etc slash config slash settings dot yaml.",
    # KEY RULES (38-52s)
    "Four rules before you use them.",
    "Not for secrets. There is no encryption. Never store passwords here.",
    "Size cap: one megabyte. Bigger than that, use a volume or external storage.",
    "Namespace-scoped. The ConfigMap must live in the same namespace as the Pod.",
    "Since version 1.19, you can mark a ConfigMap immutable. No accidental overwrites. Lighter on the API server.",
    # PAYOFF (52-62s)
    "One image.",
    "Three environments.",
    "Three ConfigMaps.",
    "Zero rebuilds.",
    # OUTRO
    "kubernetes dot configmaps.",
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
output_path = '/tmp/k8s_ep6_voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)
print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

total_frames = int(np.ceil((current_time + 4.0) * 30))  # +4s outro hold, 30fps

timing_path = '/tmp/k8s_ep6_timing.json'
with open(timing_path, 'w') as f:
    json.dump({
        "segments": segments,
        "total_voice_duration": round(current_time, 4),
        "total_duration": round(current_time + 4.0, 4),
        "total_frames_30fps": total_frames,
    }, f, indent=2)
print(f"Saved timing: {timing_path}")
print(f"Total frames at 30fps: {total_frames}")
print("\nTiming summary:")
for seg in segments:
    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text'][:70]}")
