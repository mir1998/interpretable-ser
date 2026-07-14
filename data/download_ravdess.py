"""Download the RAVDESS speech-audio dataset.

RAVDESS = Ryerson Audio-Visual Database of Emotional Speech and Song.
We use the speech, audio-only subset: 24 actors x 60 clips = 1,440 WAV files,
labelled with 8 emotions (the emotion is encoded in each filename).

Source: Zenodo record 1188976 (CC BY-NC-SA 4.0).

Usage:
    python data/download_ravdess.py

Downloads ~200 MB and extracts to data/ravdess/. Idempotent: skips if present.
"""
import os
import sys
import zipfile
import urllib.request

URL = "https://zenodo.org/records/1188976/files/Audio_Speech_Actors_01-24.zip?download=1"
HERE = os.path.dirname(os.path.abspath(__file__))
ZIP_PATH = os.path.join(HERE, "Audio_Speech_Actors_01-24.zip")
OUT_DIR = os.path.join(HERE, "ravdess")


def _count_wavs(root):
    return sum(1 for _, _, files in os.walk(root) for f in files if f.endswith(".wav"))


def _progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        pct = min(100.0, downloaded * 100.0 / total_size)
        sys.stdout.write(f"\r  downloading... {pct:5.1f}%  ({downloaded / 1e6:6.0f} MB)")
    else:
        sys.stdout.write(f"\r  downloading... {downloaded / 1e6:6.0f} MB")
    sys.stdout.flush()


def main():
    if os.path.isdir(OUT_DIR) and _count_wavs(OUT_DIR) > 0:
        print(f"RAVDESS already present in {OUT_DIR} ({_count_wavs(OUT_DIR)} wavs) - skipping.")
        return

    os.makedirs(OUT_DIR, exist_ok=True)

    if not os.path.exists(ZIP_PATH):
        print("Downloading RAVDESS speech audio from Zenodo (~200 MB)...")
        urllib.request.urlretrieve(URL, ZIP_PATH, _progress)
        print()

    print("Extracting...")
    with zipfile.ZipFile(ZIP_PATH) as z:
        z.extractall(OUT_DIR)

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    print(f"Done. {_count_wavs(OUT_DIR)} .wav files in {OUT_DIR}")


if __name__ == "__main__":
    main()
