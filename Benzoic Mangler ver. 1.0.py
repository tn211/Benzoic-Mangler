import wave
import array
import random
import librosa
import numpy as np

def estimate_bpm(samples, sr):
    # Convert the samples to floating-point values
    samples = samples.astype(np.float32)

    # Estimate the BPM using librosa's tempo estimation function
    tempo, _ = librosa.beat.beat_track(y=samples, sr=sr)

    return int(round(tempo))

def mangle_wav_file(input_file, output_file):
    with wave.open(input_file, 'rb') as wav_in:
        num_channels = wav_in.getnchannels()
        sample_width = wav_in.getsampwidth()
        sample_rate = wav_in.getframerate()

        # Read audio data from input file
        audio_data = wav_in.readframes(wav_in.getnframes())

    # Convert audio data to array of samples
    samples = array.array('h', audio_data)
    samples = np.array(samples)

    # Estimate the BPM of the input audio
    bpm = estimate_bpm(samples, sample_rate)
    print("Estimated BPM:", bpm)

    # Calculate the number of frames per slice based on the desired duration
    slice_duration = 0.6  # Duration of each slice in seconds
    slice_size = int(slice_duration * sample_rate)

    # Calculate the number of slices
    num_slices = len(samples) // slice_size

    # Create an array to store the sliced audio
    slices = np.zeros((num_slices, slice_size), dtype=np.int16)

    # Slice the audio into smaller segments
    for i in range(num_slices):
        start = i * slice_size
        end = start + slice_size
        slices[i] = samples[start:end]

    # Shuffle the audio slices based on the BPM
    random.seed(bpm)
    random.shuffle(slices)

    # Flatten the array of slices into a single array
    output_samples = slices.flatten()

    # Write the altered audio data to the output file
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setnchannels(num_channels)
        wav_out.setsampwidth(sample_width)
        wav_out.setframerate(sample_rate)
        wav_out.writeframes(output_samples.tobytes())

    print("Output WAV file generated:", output_file)

def main():
    print()
    print("Welcome to Benzoic Mangler ver. 1.0")
    print()
    input_file = input("Enter the path to the input WAV file: ")
    output_file = input("Enter the name of the output WAV file: ")
    mangle_wav_file(input_file, output_file)

if __name__ == "__main__":
    main()
