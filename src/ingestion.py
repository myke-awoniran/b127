import os
import subprocess
import soundfile as sf
import numpy as np


def generate_and_load_lossy_variants(reference_path):
    test_bench_dir = os.path.dirname(reference_path)

    codec_targets = {
        "mp3_320": {"ext": ".mp3", "args": ["-c:a", "libmp3lame", "-b:a", "320k", "-ac", "2"]},
        "aac_128": {"ext": ".m4a", "args": ["-c:a", "aac", "-b:a", "128k", "-ac", "2"]},
        "aac_256": {"ext": ".m4a", "args": ["-c:a", "aac", "-b:a", "256k", "-ac", "2"]},
        "ogg_192": {"ext": ".ogg", "args": ["-c:a", "vorbis", "-b:a", "192k", "-ac", "2", "-strict", "-2"]}
    }

    if not os.path.exists(reference_path):
        raise FileNotFoundError(f"Critical Error: Cannot find the file at {reference_path}")

    ref_data, ref_samplerate = sf.read(reference_path)
    if len(ref_data.shape) > 1:
        ref_data = np.mean(ref_data, axis=1)  # Downmix stereo to mono

    # Peak normalize the reference signal to a floating point scale (-1.0 to 1.0)
    if np.max(np.abs(ref_data)) > 0:
        ref_data = ref_data / np.max(np.abs(ref_data))

    loaded_streams = {"reference": ref_data}

    print(" -> Executing background FFmpeg compression blocks...")
    for label, config in codec_targets.items():
        compressed_native_file = os.path.join(test_bench_dir, f"temp_{label}{config['ext']}")
        decoded_wav_file = os.path.join(test_bench_dir, f"temp_decoded_{label}.wav")

        # Step A: Compress natively into target container
        subprocess.run(["ffmpeg", "-y", "-i", reference_path, *config["args"], compressed_native_file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Step B: Decode back to standard Linear PCM WAV
        subprocess.run(["ffmpeg", "-y", "-i", compressed_native_file, "-f", "wav", "-ac", "1", decoded_wav_file],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        comp_data, comp_samplerate = sf.read(decoded_wav_file)
        if len(comp_data.shape) > 1:
            comp_data = np.mean(comp_data, axis=1)

        # Peak normalize the compressed target to match the reference float scale perfectly
        if np.max(np.abs(comp_data)) > 0:
            comp_data = comp_data / np.max(np.abs(comp_data))

        if comp_samplerate != ref_samplerate:
            raise ValueError(f"Codec {label} altered the sampling rate! Math cannot proceed.")

        loaded_streams[label] = comp_data

        # Clean up temporary disk files
        for temp_file in [compressed_native_file, decoded_wav_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    return loaded_streams, ref_samplerate
