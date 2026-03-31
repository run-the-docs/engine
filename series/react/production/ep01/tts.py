#!/usr/bin/env python3
"""Generate TTS for React ep01: Your First Component (EXPANDED to cover all concepts)"""
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
GAP = 0.38

sentences = [
    # INTRO (0-4s)
    "React is built on components. They're the foundation of every user interface you build.",
    "A component is a reusable piece of UI — like a button, a card, or a sidebar.",
    "It can be as small as a button, or as large as an entire page.",
    "Just like HTML has tags like div and button, React lets you create your own custom components.",
    
    # FUNCTIONS (4-12s)
    "Here's the key idea: a React component is just a JavaScript function.",
    "It's a function that returns markup — HTML-like code called JSX.",
    "Let's call our function MyButton. It returns a button element.",
    "That's it. Function. Return markup. That's a component.",
    
    # EXPORT (12-23s)
    "To use your component in other files, you need to export it.",
    "First: add the export default prefix before your function.",
    "This tells JavaScript that MyButton is the main thing this file exports.",
    "You can learn more about imports and exports in the next episode.",
    "For now, just remember: export default makes your component reusable.",
    
    # USING (23-32s)
    "Now that you've defined MyButton, you can use it anywhere in your app.",
    "Reference it like you would any JSX element. That's capital M, capital B: MyButton.",
    "The capital letter matters. React uses capitalization to tell components apart from HTML tags.",
    "So div is lowercase — that's an HTML tag. MyButton is capitalized — that's your component.",
    
    # NESTING (32-45s)
    "Components can contain other components. That's called nesting.",
    "You can use MyButton inside a Gallery component, multiple times.",
    "Each MyButton is independent. Each one can have its own state later.",
    "You can build entire pages this way — one component inside another, all the way down.",
    
    # BEST PRACTICES (45-60s)
    "Important rule: never define a component inside another component.",
    "If you define MyButton inside Gallery, your app will be slow and buggy.",
    "Always define components at the top level, outside of other functions.",
    "If a child component needs data from a parent, pass it with props instead.",
    
    # ALL THE WAY DOWN (60-72s)
    "Your React app starts with a root component.",
    "Most React apps use components all the way down.",
    "Not just for small things like buttons, but for large sections like sidebars and pages.",
    "Components are how you organize and structure your entire UI.",
    
    # RECAP (72-83s)
    "Here's what you learned: React components are JavaScript functions that return markup.",
    "They let you build reusable UI pieces.",
    "Capitalize their names. Export them to reuse them. Nest them to build complex interfaces.",
    "You're ready for the next concept: Props.",
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

# Add outro silence (CRITICAL: must be in the WAV file for sync)
outro_samples = int(4.0 * SAMPLE_RATE)  # 4s outro buffer
all_audio.append(np.zeros(outro_samples, dtype=np.float32))

final_audio = np.concatenate(all_audio)
output_path = 'voice.wav'
sf.write(output_path, final_audio, SAMPLE_RATE)
print(f"\nSaved: {output_path}")
print(f"Total voice duration: {current_time:.2f}s")

total_frames = int(np.ceil((current_time + 4.0) * 30))  # +4s outro, 30fps

timing_path = 'timing.json'
with open(timing_path, 'w') as f:
    json.dump({
        "segments": segments,
        "total_voice_duration": round(current_time, 4),
        "total_duration": round(current_time + 4.0, 4),
        "total_frames_30fps": total_frames,
    }, f, indent=2)
print(f"Saved timing: {timing_path}")
print(f"Total frames at 30fps: {total_frames}")
print(f"\nTiming summary:")
for seg in segments:
    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text'][:60]}")
