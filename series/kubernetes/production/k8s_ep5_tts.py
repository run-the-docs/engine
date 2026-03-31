#!/usr/bin/env python3
"""Generate TTS for Kubernetes Ep5: Services"""
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
    # HOOK (0-5s)
    "Pods die and get replaced. Their IPs change.",
    "Services don't.",
    # PROBLEM (5-18s)
    "Here's the problem.",
    "Your frontend hardcodes a backend Pod IP.",
    "That Pod dies. A new one starts with a different IP. Your frontend breaks.",
    "Services fix this with a stable virtual IP and DNS name.",
    # HOW IT WORKS (18-35s)
    "Add a selector to match Pods by label.",
    "Kubernetes creates a ClusterIP — a stable virtual address.",
    "kube-proxy writes network rules on every node.",
    "Traffic hits the Service IP. It routes to a healthy Pod.",
    "EndpointSlices track which Pods back the Service — updated automatically.",
    # SERVICE TYPES (35-52s)
    "Four Service types.",
    "ClusterIP — internal only. The default.",
    "NodePort — exposes on each node, port 30000 to 32767.",
    "LoadBalancer — cloud provider creates an external load balancer.",
    "ExternalName — maps to an external DNS name.",
    # PAYOFF (52-62s)
    "One Service. Many Pods. Zero hardcoded IPs.",
    "That's how Kubernetes decouples your frontend from your backend.",
    # OUTRO (62-72s)
    "Run the Docs. Kubernetes. Services.",
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
output_path = '/tmp/k8s_ep5_voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)
print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

total_frames = int(np.ceil((current_time + 4.0) * 30))  # +4s outro, 30fps

timing_path = '/tmp/k8s_ep5_timing.json'
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
