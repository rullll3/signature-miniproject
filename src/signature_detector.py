import argparse
from pathlib import Path
import cv2
import numpy as np
import pandas as pd

# ROI: signature of the "Dekan" on the supplied certificate layout.
# Coordinates are based on the 1536x1087 images provided for this mini-project.
CROP = (950, 770, 1350, 875)  # x1, y1, x2, y2
GLOBAL_THRESHOLD = 180
MIN_FOREGROUND_RATIO = 0.03
MAX_OTSUS_FOREGROUND_RATIO = 0.40
UNRELIABLE_OTSU_THRESHOLD = 230


def crop_signature(gray, crop=CROP):
    x1, y1, x2, y2 = crop
    return gray[y1:y2, x1:x2]


def threshold_global(roi, threshold=GLOBAL_THRESHOLD):
    _, binary = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY_INV)
    return binary


def threshold_otsu(roi):
    threshold, binary = cv2.threshold(
        roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    return int(threshold), binary


def morphology(binary):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    return closed


def foreground_count(binary):
    return int(np.count_nonzero(binary))


def detect_signature(roi):
    global_bin = threshold_global(roi)
    otsu_threshold, otsu_bin = threshold_otsu(roi)

    global_morph = morphology(global_bin)
    otsu_morph = morphology(otsu_bin)

    global_fg = foreground_count(global_morph)
    otsu_fg = foreground_count(otsu_morph)
    total = otsu_morph.size

    global_ratio = global_fg / total
    otsu_ratio = otsu_fg / total

    # Otsu is preferred for uneven/dark scans, but it can fail on a
    # nearly uniform blank ROI by treating the background as foreground.
    otsu_reliable = (
        otsu_threshold <= UNRELIABLE_OTSU_THRESHOLD
        and otsu_ratio <= MAX_OTSUS_FOREGROUND_RATIO
    )

    if otsu_reliable:
        selected_method = "Otsu"
        selected_binary = otsu_morph
        selected_fg = otsu_fg
        selected_ratio = otsu_ratio
    else:
        selected_method = "Global (fallback)"
        selected_binary = global_morph
        selected_fg = global_fg
        selected_ratio = global_ratio

    label = (
        "SIGNATURE PRESENT"
        if selected_ratio >= MIN_FOREGROUND_RATIO
        else "SIGNATURE ABSENT"
    )

    return {
        "global_threshold": GLOBAL_THRESHOLD,
        "otsu_threshold": otsu_threshold,
        "global_foreground": global_fg,
        "global_ratio": global_ratio,
        "otsu_foreground": otsu_fg,
        "otsu_ratio": otsu_ratio,
        "selected_method": selected_method,
        "selected_foreground": selected_fg,
        "selected_ratio": selected_ratio,
        "prediction": label,
        "binary": selected_binary,
        "global_binary": global_morph,
        "otsu_binary": otsu_morph,
    }


def process_image(path):
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Cannot read image: {path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    roi = crop_signature(gray)
    result = detect_signature(roi)
    result["file"] = Path(path).name
    return result


def run_dataset(dataset_dir, output_csv):
    dataset_dir = Path(dataset_dir)
    rows = []

    for label_dir in sorted(dataset_dir.iterdir()):
        if not label_dir.is_dir():
            continue
        expected = "SIGNATURE PRESENT" if label_dir.name.lower() == "present" else "SIGNATURE ABSENT"
        for path in sorted(label_dir.glob("*.jpg")):
            result = process_image(path)
            rows.append({
                "file": result["file"],
                "expected": expected,
                "prediction": result["prediction"],
                "selected_method": result["selected_method"],
                "global_threshold": result["global_threshold"],
                "otsu_threshold": result["otsu_threshold"],
                "global_foreground": result["global_foreground"],
                "global_ratio": round(result["global_ratio"], 4),
                "otsu_foreground": result["otsu_foreground"],
                "otsu_ratio": round(result["otsu_ratio"], 4),
                "selected_foreground": result["selected_foreground"],
                "selected_ratio": round(result["selected_ratio"], 4),
            })

    df = pd.DataFrame(rows)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    if len(df):
        accuracy = (df["expected"] == df["prediction"]).mean()
        print(df.to_string(index=False))
        print(f"\nAccuracy: {accuracy:.2%}")
    return df


def save_comparison(image_path, output_path):
    result = process_image(image_path)
    roi = crop_signature(
        cv2.cvtColor(cv2.imread(str(image_path)), cv2.COLOR_BGR2GRAY)
    )

    panels = [
        ("Grayscale crop", roi),
        ("Global threshold", result["global_binary"]),
        ("Otsu threshold", result["otsu_binary"]),
        ("Otsu + opening + closing", result["binary"]),
    ]

    rendered = []
    for title, img in panels:
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.putText(
            vis, title, (8, 22), cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (0, 0, 0), 2, cv2.LINE_AA
        )
        rendered.append(vis)

    comparison = cv2.hconcat(rendered)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), comparison)


def main():
    parser = argparse.ArgumentParser(description="Signature presence detector")
    parser.add_argument("--dataset", default="data/test")
    parser.add_argument("--output", default="outputs/results.csv")
    parser.add_argument("--comparison", default="outputs/comparison.png")
    args = parser.parse_args()

    df = run_dataset(args.dataset, args.output)

    # Use the first available positive sample for the visual comparison.
    positives = sorted(Path(args.dataset, "present").glob("*.jpg"))
    if positives:
        save_comparison(positives[0], args.comparison)


if __name__ == "__main__":
    main()
