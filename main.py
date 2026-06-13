import os
import sys
import subprocess
from src.ingestion import generate_and_load_lossy_variants
from src.transform import generate_codec_residuals
from src.visualization import export_codec_comparison_grid


def bootstrap_environment():
    project_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(project_file_path)
    venv_dir = os.path.join(project_root, ".venv")
    is_venv = sys.prefix != sys.base_prefix or "VIRTUAL_ENV" in os.environ

    if not is_venv:
        print("Project B127: Invoking isolated execution workspace...")
        if not os.path.exists(venv_dir):
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)

        venv_python = os.path.join(venv_dir, "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(
            venv_dir, "bin", "python3")
        arguments = [venv_python] + sys.argv
        os.execv(venv_python, arguments)

    try:
        import numpy, scipy, soundfile, matplotlib
    except ImportError:
        print(" -> Syncing local pipeline modules inside the sandbox...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-q",
            "numpy>=1.20.0", "scipy>=1.7.0", "soundfile>=0.10.0", "matplotlib>=3.4.0"
        ], check=True)


# Run the environment bootstrapper immediately
bootstrap_environment()


def execute_analysis_pipeline():
    print("Initializing Project B127 Forensic Benchmarking Suite...")

    reference_file = "test_bench/reference.flac"
    output_grid_image = "test_bench/codec_comparison_residual.png"

    if not os.path.exists(reference_file):
        print(f"\n[Error] Missing master reference target: {reference_file}")
        sys.exit(1)

    print("Step 1: Instantiating automated multi-format encoding pipelines via FFmpeg...")
    audio_streams, samplerate = generate_and_load_lossy_variants(reference_file)

    print("Step 2: Processing Short-Time Fourier Transforms and parsing alignment conditions...")
    freqs, times, residuals_dict = generate_codec_residuals(audio_streams, samplerate)

    print("Step 3: Plotting 2x2 diagnostic spectrogram matrices...")
    export_codec_comparison_grid(freqs, times, residuals_dict, output_grid_image)

    print(f"\n[Success] Analysis Complete! Visual grid map saved to: {output_grid_image}")


if __name__ == "__main__":
    execute_analysis_pipeline()
