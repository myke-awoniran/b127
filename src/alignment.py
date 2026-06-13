import numpy as np
from scipy.signal import correlate


def synchronize_time_arrays(reference_signal, compressed_signal):
    max_search_size = min(len(reference_signal), len(compressed_signal), 44100 * 5)
    ref_chunk = reference_signal[:max_search_size]
    comp_chunk = compressed_signal[:max_search_size]

    cross_correlation = correlate(ref_chunk, comp_chunk, mode="full")
    lag_indices = np.arange(-max_search_size + 1, max_search_size)
    calculated_sample_lag = lag_indices[np.argmax(cross_correlation)]

    if calculated_sample_lag > 0:
        aligned_reference = reference_signal[calculated_sample_lag:]
        aligned_compressed = compressed_signal[:len(aligned_reference)]
    elif calculated_sample_lag < 0:
        lag_absolute = abs(calculated_sample_lag)
        aligned_compressed = compressed_signal[lag_absolute:]
        aligned_reference = reference_signal[:len(aligned_compressed)]
    else:
        minimum_length = min(len(reference_signal), len(compressed_signal))
        aligned_reference = reference_signal[:minimum_length]
        aligned_compressed = compressed_signal[:minimum_length]

    return aligned_reference, aligned_compressed
