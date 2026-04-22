from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_subhistograms(pattern: str = "subhist_*.npy") -> list[Path]:
    histogram_paths = sorted(Path(".").glob(pattern))
    if not histogram_paths:
        raise FileNotFoundError(f"No histogram files matched pattern: {pattern}")
    return histogram_paths


def combine_histograms(histogram_paths: list[Path]) -> np.ndarray:
    total_hist = np.zeros(64, dtype=np.int64)

    for path in histogram_paths:
        hist = np.load(path)
        if hist.shape != (64,):
            raise ValueError(f"Unexpected histogram shape in {path}: {hist.shape}")
        total_hist += hist

    return total_hist


def save_plot(histogram: np.ndarray, output_path: Path) -> None:
    bin_edges = np.linspace(0, 255, 64 + 1)
    bin_width = bin_edges[1] - bin_edges[0]

    plt.figure(figsize=(12, 5))
    plt.bar(bin_edges[:-1], histogram, width=bin_width, align="edge")
    plt.xlabel("Hue value")
    plt.ylabel("Pixel count")
    plt.title("CelebA Hue Histogram")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    histogram_paths = load_subhistograms()
    total_hist = combine_histograms(histogram_paths)

    np.save("combined_hist.npy", total_hist)
    save_plot(total_hist, Path("combined_hist.png"))

    print(f"Loaded {len(histogram_paths)} sub-histograms")
    print("Saved combined histogram to: combined_hist.npy")
    print("Saved histogram plot to: combined_hist.png")


if __name__ == "__main__":
    main()
