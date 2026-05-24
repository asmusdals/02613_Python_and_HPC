from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


DATA_ROOT = Path("/dtu/projects/02613_2024/data/celeba/images")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp"}


def huehist(image: np.ndarray) -> np.ndarray:
    bins = np.linspace(0, 255, 64 + 1)
    hsv_image = np.asarray(Image.fromarray(image).convert("HSV"))
    hue_values = hsv_image[:, :, 0].reshape(-1)
    hue_hist = np.histogram(hue_values, bins)[0]
    return hue_hist


def list_subfolders(root: Path) -> list[Path]:
    if not root.is_dir():
        raise FileNotFoundError(f"Dataset folder not found: {root}")
    return sorted(path for path in root.iterdir() if path.is_dir())


def list_images(folder: Path) -> list[Path]:
    return sorted(
        path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def folder_histogram(folder: Path) -> np.ndarray:
    total_hist = np.zeros(64, dtype=np.int64)
    image_paths = list_images(folder)

    if not image_paths:
        raise ValueError(f"No supported image files found in {folder}")

    for image_path in image_paths:
        with Image.open(image_path) as img:
            rgb_image = np.asarray(img.convert("RGB"))
        total_hist += huehist(rgb_image)

    return total_hist


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute a summed hue histogram for the i'th CelebA image subfolder."
    )
    parser.add_argument(
        "index",
        type=int,
        help="1-based subfolder index. Use LSB_JOBINDEX when running as an HPC job array.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.index < 1:
        raise ValueError("Index must be >= 1 because LSF job arrays are 1-based.")

    subfolders = list_subfolders(DATA_ROOT)
    if args.index > len(subfolders):
        raise IndexError(
            f"Index {args.index} is out of range. Found {len(subfolders)} subfolders in {DATA_ROOT}."
        )

    folder = subfolders[args.index - 1]
    total_hist = folder_histogram(folder)

    output_path = Path(f"subhist_{args.index}.npy")
    np.save(output_path, total_hist)

    print(f"Processed folder {args.index}: {folder.name}")
    print(f"Images processed: {len(list_images(folder))}")
    print(f"Saved histogram to: {output_path}")


if __name__ == "__main__":
    main()
