import soundfile as sf
import json
import numpy as np
import types
from scipy.signal import resample as scipy_resample
from kokoro_onnx import Kokoro, MAX_PHONEME_LENGTH, SAMPLE_RATE

kokoro = Kokoro(
    '/Users/claude/runthedocs/kokoro/onnx/model.onnx',
    '/Users/claude/runthedocs/kokoro/voices.npz'
)

def patched(self, phonemes, voice, speed):
    phonemes = phonemes[:MAX_PHONEME_LENGTH]
    tokens = np.array(self.tokenizer.tokenize(phonemes), dtype=np.int64)
    style = voice[len(tokens)]
    return self.sess.run(None, {
        'input_ids': [[0, *tokens, 0]],
        'style': np.array(style, dtype=np.float32).reshape(1, -1),
        'speed': np.array([speed], dtype=np.float32)
    })[0], SAMPLE_RATE

kokoro._create_audio = types.MethodType(patched, kokoro)

sentences = [
    "React can render lists from arrays. You need JavaScript's map method — that's it.",
    "Call array dot map, pass a function, return JSX. React renders one element per item.",
    "Each list item needs a key prop. Keys help React track which items changed, were added, or removed.",
    "Keys must be unique among siblings. They don't need to be globally unique — just within that list.",
    "Use stable IDs from your data as keys. Database IDs are ideal.",
    "Don't use array indexes as keys unless the list never changes order. Index keys break when items move.",
    "Never use Math dot random as a key. It changes every render and destroys performance.",
    "Keys are not passed as props. If your component needs the ID, pass it as a separate prop with a different name.",
    "You can filter and map together. Call array dot filter first, then dot map on the result.",
    "JSX lets you embed the whole map expression inside curly braces, right in the return statement.",
    "If your list items need more than one DOM element, wrap them in a Fragment. Fragments let you add a key without adding extra DOM nodes.",
    "Nested lists work the same way. Map inside map, each with its own key.",
    "React shows a warning in the console if keys are missing. Take it seriously — it means list updates will be slow or incorrect.",
    "Let's recap. Use map to render lists. Give every item a stable key. Avoid indexes and random values.",
    "Next up: keeping components pure.",
]

TARGET_SR = 44100
INTRO_SILENCE = 2.0
GAP = 0.38
OUTRO = 4.0

def make_silence(duration_s, sr):
    return np.zeros(int(duration_s * sr), dtype=np.float32)

segments = []
all_chunks = []

# Intro silence
intro_samples = make_silence(INTRO_SILENCE, TARGET_SR)
all_chunks.append(intro_samples)
cursor = INTRO_SILENCE

for i, text in enumerate(sentences):
    print(f"Synthesizing sentence {i+1}/{len(sentences)}: {text[:50]}...")
    audio, sr = kokoro.create(text, voice="bm_george", speed=1.0, lang="en-us")
    audio = np.array(audio).astype(np.float32)
    if audio.ndim > 1:
        audio = audio.squeeze()

    # Resample from native SAMPLE_RATE to 44100
    if sr != TARGET_SR:
        num_samples = int(len(audio) * TARGET_SR / sr)
        audio = scipy_resample(audio, num_samples).astype(np.float32)

    duration = len(audio) / TARGET_SR
    start = cursor
    end = start + duration

    segments.append({
        "index": i,
        "text": text,
        "start": round(start, 3),
        "end": round(end, 3),
        "duration": round(duration, 3),
    })

    all_chunks.append(audio)
    cursor = end

    if i < len(sentences) - 1:
        gap_samples = make_silence(GAP, TARGET_SR)
        all_chunks.append(gap_samples)
        cursor += GAP

# Outro silence
outro_samples = make_silence(OUTRO, TARGET_SR)
all_chunks.append(outro_samples)
total_duration = cursor + OUTRO

final_audio = np.concatenate(all_chunks)

sf.write("voice.wav", final_audio, TARGET_SR)
print(f"Saved voice.wav ({len(final_audio)/TARGET_SR:.2f}s)")

total_voice_duration = segments[-1]["end"] if segments else 0
timing = {
    "total_voice_duration": round(total_voice_duration, 3),
    "total_duration": round(total_duration, 3),
    "total_frames_30fps": int(total_duration * 30),
    "sample_rate": TARGET_SR,
    "segments": segments,
}

with open("timing.json", "w") as f:
    json.dump(timing, f, indent=2)
print(f"Saved timing.json — {timing['total_frames_30fps']} frames at 30fps")
