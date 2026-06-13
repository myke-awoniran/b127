import numpy as np
from scipy.signal import stft
from src.alignment import synchronize_time_arrays


def generate_codec_residuals(streams_dictionary, samplerate):
    window_length = 2048
    hop_size = 512

    target_codecs = ["mp3_320", "aac_128", "aac_256", "ogg_192"]
    aligned_streams = {}

    # Cross-correlate timelines relative to the reference signal
    for codec in target_codecs:
        _, aligned_comp = synchronize_time_arrays(streams_dictionary["reference"], streams_dictionary[codec])
        aligned_streams[codec] = aligned_comp

    aligned_ref, _ = synchronize_time_arrays(streams_dictionary["reference"], streams_dictionary["mp3_320"])
    aligned_streams["reference"] = aligned_ref

    # Slice all variants to match the absolute minimum overlapping sample length
    min_length = min(len(arr) for arr in aligned_streams.values())
    for key in aligned_streams.keys():
        aligned_streams[key] = aligned_streams[key][:min_length]

    # Compute reference STFT grid size
    frequencies, times, ref_complex_matrix = stft(aligned_streams["reference"], fs=samplerate, window="hann",
                                                  nperseg=window_length, noverlap=window_length - hop_size)
    ref_magnitude = np.abs(ref_complex_matrix)

    residual_matrices = {}

    # Generate residuals safely against uniform grids
    for codec in target_codecs:
        _, _, comp_complex_matrix = stft(aligned_streams[codec], fs=samplerate, window="hann", nperseg=window_length,
                                         noverlap=window_length - hop_size)
        comp_magnitude = np.abs(comp_complex_matrix)

        # Capture absolute magnitude variations directly to elevate out of the visual floor
        residual = np.abs(ref_magnitude - comp_magnitude)
        residual_matrices[codec] = residual

    return frequencies, times, residual_matrices
