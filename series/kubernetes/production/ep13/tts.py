#!/usr/bin/env python3
"""TTS for K8s ep13 Short: Labels & Selectors (under 60s)"""
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
    inputs = {
        'input_ids': [[0, *tokens, 0]],
        'style': np.array(style, dtype=np.float32).reshape(1, -1),
        'speed': np.array([speed], dtype=np.float32),
    }
    audio = self.sess.run(None, inputs)[0]
    return audio, SAMPLE_RATE

kokoro._create_audio = types.MethodType(patched_create_audio, kokoro)

INTRO_SILENCE = 2.0
GAP = 0.38
OUTRO_BUFFER = 4.0
VOICE = 'bm_george'

sentences = [
    # HOOK (0–2s intro, 2–6s)
    "Labels are key-value pairs attached to any Kubernetes object.",
    # MOTIVATION (6–18s)
    "They don't mean anything to the system — but they're how you organize everything.",
    "Environment: production. Tier: frontend. Release: canary.",
    "Any object can have multiple labels. Many objects can share the same label.",
    # SELECTORS (18–40s)
    "Label selectors let you query objects by those labels.",
    "Equality-based: environment equals production, tier not-equals frontend.",
    "Set-based: environment in production or Q-A. Tier not-in backend.",
    "In kubectl: kubectl get pods -l environment equals production.",
    # PAYOFF (40–52s)
    "Services use selectors to route traffic to matching Pods.",
    "ReplicaSets use them to track which Pods they own.",
    # OUTRO (52–56s, then 4s buffer)
    "Labels and selectors: the query language of Kubernetes.",
]

print(f"Generating {len(sentences)} sentences ({VOICE})...")
segments = []
all_audio = [np.zeros(int(INTRO_SILENCE * SAMPLE_RATE), dtype=np.float32)]
current_time = INTRO_SILENCE

for i, sentence in enumerate(sentences):
    print(f"  [{i+1}/{len(sentences)}] {sentence[:70]}")
    audio, sr = kokoro.create(sentence, voice=VOICE, speed=1.0, lang='en-us')
    audio_flat = audio.flatten()
    start = current_time
    duration = len(audio_flat) / sr
    end = start + duration
    segments.append({"index": i, "text": sentence, "start": round(start, 4),
                     "end": round(end, 4), "duration": round(duration, 4)})
    all_audio.append(audio_flat)
    current_time = end
    if i < len(sentences) - 1:
        all_audio.append(np.zeros(int(GAP * SAMPLE_RATE), dtype=np.float32))
        current_time += GAP

all_audio.append(np.zeros(int(OUTRO_BUFFER * SAMPLE_RATE), dtype=np.float32))

final_audio = np.concatenate(all_audio)
sf.write('voice.wav', final_audio, SAMPLE_RATE)
print(f"\nSaved voice.wav ({current_time:.2f}s narration)")

total_duration = current_time + OUTRO_BUFFER
total_frames = int(np.ceil(total_duration * 30))

with open('timing.json', 'w') as f:
    json.dump({
        "segments": segments,
        "total_voice_duration": round(current_time, 4),
        "total_duration": round(total_duration, 4),
        "total_frames_30fps": total_frames,
    }, f, indent=2)

print(f"Saved timing.json — {total_duration:.2f}s total ({total_frames} frames @ 30fps)")
print("\nTiming summary:")
for seg in segments:
    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text'][:60]}")
