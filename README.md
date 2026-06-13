# Project B127
<img src="assets/images/b127.jpg" alt="Alternative text" width="500" />

B127 is a specialized forensic digital signal processing application designed to expose and visualise exactly what lossy audio encoders like MP3, AAC, or Ogg Vorbis throw away during compression.

When audio is compressed into these formats, algorithms permanently delete data that the human ear allegedly cannot perceive. B127 acts as an audio archeologist. It takes a perfect, lossless reference file like a FLAC and its compressed counterpart, mathematically aligns them down to the exact sample to eliminate time delays, converts both into the frequency domain, and subtracts them.

The resulting visual map, known as a **spectral residual**, isolates the ghost data, which represents the precise frequencies and acoustic footprints that the compression engine deemed unnecessary.

---

## The Problem

The fundamental problem B127 addresses is lossy data reduction transparency.

Psychoacoustic models operate on the principle of auditory masking. If there is a loud sound at 1 kHz, your brain cannot hear a quieter sound at 1.1 kHz occurring at the same time. Lossy encoders exploit this limitation to save file space by stripping out the hidden, masked frequencies.

However, verifying exactly how these encoders alter audio, or analyzing the deterministic artifacts they leave behind, is incredibly difficult because lossy encoders introduce minute, random padding samples at the start of a file, an effect called **stream head priming**. This shifts the timeline slightly. 

Without correcting this phase misalignment, a direct file comparison results in chaotic noise rather than a precise profile of the discarded data. B127 solves this synchronization problem to isolate the exact psychoacoustic masking threshold used by the encoder.

---

## Nyquist Sampling Theory and The 44.1 kHz Standard

To understand why these files are structured this way, we have to look at how continuous, real world analog sound waves are converted into discrete digital numbers.

### The Nyquist Shannon Sampling Theorem

The theorem states that to perfectly reconstruct an analog signal without distortion, the sampling rate ($f_s$) must be greater than twice the highest frequency component ($f_{max}$) present within that signal.

$$f_s > 2 \cdot f_{max}$$

The highest frequency that a given digital sampling rate can accurately capture is called the **Nyquist Frequency**:

$$\text{Nyquist Frequency} = \frac{f_s}{2}$$

If an analog signal contains frequencies higher than the Nyquist Frequency when it is sampled, those high frequencies fold back into the lower spectrum. This creates a destructive type of digital distortion called **aliasing**, which manifests as false lower frequencies that were not there in reality.

### Why CDs Use 44.1 kHz for Human Hearing

The standard human hearing range is universally accepted to be between 20 Hz and 20,000 Hz (20 kHz).

To digitalize the absolute upper limit of human hearing (20 kHz) without aliasing, the absolute bare minimum sampling rate required by the Nyquist theorem is:

$$2 \cdot 20 \text{ kHz} = 40 \text{ kHz}$$

CD engineers settled on 44.1 kHz instead of a clean 40 kHz due to two primary engineering reasons:

1. **Anti Aliasing Filter Transition Bands:** In the early days of digital audio, analog low pass filters were used before the sampling phase to aggressively cut off any frequencies above 20 kHz so they would not cause aliasing. Real world filters cannot drop off like a perfectly sharp brick wall. They require a physical slope or transition zone to roll off smoothly from 0 dB to total silence. The extra 4.1 kHz of headroom, which is the space between 20 kHz and 22.05 kHz, provides a safety buffer for the analog filters to attenuate the signal completely without damaging the audible frequencies under 20 kHz.
2. **Video Format Compatibility:** When Compact Discs were being standardized in the late 1970s and early 1980s by Sony and Philips, digital audio data had to be stored on modified industrial video tape recorders because digital disk storage did not exist yet. The video standards of the era were PAL running at 50 Hz and NTSC running at 60 Hz. Engineers needed a sampling frequency that could cleanly map across both video formats without complex fractional math.

* **For PAL:** $$\text{294 lines per frame} \times \text{3 samples per line} \times \text{50 frames per second} = 44,100 \text{ Hz}$$
* **For NTSC:** $$\text{245 lines per frame} \times \text{3 samples per line} \times \text{60 frames per second} = 44,100 \text{ Hz}$$

Thus, 44.1 kHz became the perfect mathematical bridge that satisfied both the biological requirements of human hearing and the limitations of early digital hardware components.