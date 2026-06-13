import matplotlib.pyplot as plt
import numpy as np


def export_codec_comparison_grid(frequencies, times, residuals_dict, output_image_path):
    """
    Plots residuals inside a highly dynamic color map to emphasize subtle loss traces.
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharex=True, sharey=True)
    axes_flattened = axes.flatten()

    panel_configurations = [
        ("mp3_320", "MP3 320 kbps (High Quality Residual Map)", 0),
        ("aac_128", "AAC 128 kbps (Low Quality Residual Map)", 1),
        ("aac_256", "AAC 256 kbps (Standard Master Residual Map)", 2),
        ("ogg_192", "Ogg Vorbis 192 kbps (Adaptive Tapering Residual Map)", 3)
    ]

    eps = 1e-10
    spectrogram_plot = None

    for key, title, index in panel_configurations:
        ax = axes_flattened[index]
        matrix_db = 20 * np.log10(residuals_dict[key] + eps)

        # Enforce 'nearest' pixel centers and use high-visibility 'inferno' contrast bounds
        spectrogram_plot = ax.pcolormesh(
            times, frequencies, matrix_db,
            shading="nearest", cmap="viridis", vmin=-50, vmax=-10
        )

        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_ylim(0, 22050)

        if index >= 2: ax.set_xlabel("Time (Seconds)")
        if index in [0, 2]: ax.set_ylabel("Frequency (Hz)")

    fig.subplots_adjust(right=0.88)
    cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])
    color_bar = fig.colorbar(spectrogram_plot, cax=cbar_ax)
    color_bar.set_label("Discarded Energy Density Scaling Floor (dB)", fontsize=11)

    plt.suptitle("Project B127: Cross-Codec Forensic Residual Benchmark Analysis", fontsize=16, fontweight="bold",
                 y=0.96)
    plt.savefig(output_image_path, dpi=300, bbox_inches="tight")
    plt.close()