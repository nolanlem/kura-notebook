import os
from typing import Iterable, List

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile


def to_mono(audio: np.ndarray) -> np.ndarray:
    if audio.ndim == 1:
        return audio
    return audio[:, 0]


def load_event_rows(npy_path: str) -> List[np.ndarray]:
    arr = np.load(npy_path, allow_pickle=True)
    rows: List[np.ndarray] = []

    if isinstance(arr, np.ndarray) and arr.dtype == object:
        for elem in arr:
            rows.append(np.asarray(elem).astype(int))
    elif arr.ndim == 1:
        rows.append(arr.astype(int))
    elif arr.ndim == 2:
        for i in range(arr.shape[0]):
            rows.append(arr[i].astype(int))
    else:
        rows.append(np.asarray(arr).astype(int))
    return rows


def main() -> None:
    base_dir = "/Users/nolanlem/Desktop/kura-notebook/stimuli_3"
    wav_filename = "strong_n_81_3.wav"
    npy_relpath = os.path.join("phases", "onsets", "strong_n_81_3.npy")

    wav_path = os.path.join(base_dir, wav_filename)
    npy_path = os.path.join(base_dir, npy_relpath)

    # 5 seconds worth of samples at 44.1 kHz (as requested: first 44100*5 samples)
    num_samples = 44100 * 5

    sr, audio = wavfile.read(wav_path)
    audio = to_mono(audio)
    audio_segment = audio[:num_samples]
    x = np.arange(audio_segment.shape[0])

    event_rows = load_event_rows(npy_path)
    # Clip events to the displayed window
    clipped_rows = [row[(row >= 0) & (row < num_samples)] for row in event_rows]

    fig, (ax_wave, ax_events) = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(12, 6),
        constrained_layout=True,
    )

    ax_wave.plot(x, audio_segment, linewidth=0.8, color="black")
    ax_wave.set_title(f"Waveform: {wav_filename} (showing first {num_samples} samples)")
    ax_wave.set_ylabel("Amplitude")

    # Plot vertical lines for each row of events; color-cycle distinguishes rows
    for idx, row in enumerate(clipped_rows):
        if row.size == 0:
            continue
        ax_events.vlines(row, ymin=0.0, ymax=1.0, colors=None, alpha=0.8, label=f"row {idx+1}")

    ax_events.set_ylim(0, 1)
    ax_events.set_yticks([])
    ax_events.set_xlabel("Sample index")
    if len(clipped_rows) > 1:
        ax_events.legend(loc="upper right", fontsize=8)
    ax_events.set_title("Event markers from phases/onsets/strong_n_81_3.npy")

    # Save figure to existing plots directory
    out_dir = os.path.join(base_dir, "plots")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "strong_n_81_3_alignment.png")
    fig.savefig(out_path, dpi=150)
    print(f"Saved alignment plot to: {out_path}")

    # Also show for interactive runs
    try:
        plt.show()
    except Exception:
        # Headless environments may not show; saving is sufficient
        pass


if __name__ == "__main__":
    main()

