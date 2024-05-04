import re
from scipy.io import wavfile
import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

file_name = 'Voice2.wav'

# Convert the file to WAV format
data, sr = sf.read(file_name)
if data.ndim > 1:
    # If the audio has multiple channels, take only the first channel
    data = data[:, 0]
sf.write('converted.wav', data, sr)

# Read the converted WAV file
data = wavfile.read('converted.wav')

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

input_audio, _ = librosa.load('converted.wav', sr=16000)

input_values = tokenizer(input_audio, return_tensors="pt").input_values
logits = model(input_values).logits

predicted_ids = torch.argmax(logits, dim=-1)

transcription = tokenizer.batch_decode(predicted_ids)[0]

print(transcription)


# Regular expression pattern to match "create" followed by "new" and capturing the word after "new"
pattern = re.compile(r'create(?:\s+a)?(?:\s+new)?\s+(\w+)', re.IGNORECASE)

text = "Create a new logo"

match = pattern.search(text)

if match:
    # Extract the word after "create new"
    word_after_create_new = match.group(1)
    print("Match found:", word_after_create_new)
else:
    print("No match found.")
