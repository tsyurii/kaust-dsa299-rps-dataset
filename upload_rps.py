#!/usr/bin/env python3
"""
upload_rps.py — upload the Rock-Paper-Scissors dataset to Edge Impulse.

Cross-platform (Windows / macOS / Linux). Solves the things that bite the bare
`edge-impulse-uploader ... *.jpg` command:
  * Windows cmd/PowerShell don't expand `*.jpg`  -> Python globs the files itself.
  * cmd.exe caps a command line at ~8191 chars    -> uploads in LENGTH-BOUNDED batches
    (a fixed file count overflows that limit and silently truncates -> partial upload).

It walks training/ and testing/, each containing rock/ paper/ scissors/ folders, and
uploads every .jpg with the correct --category (train/test) and --label (class name).

PREREQS
  1) Node + EI CLI:   npm install -g edge-impulse-cli
  2) A project set to **One label per data item** (Dashboard -> Labeling method),
     NOT object detection -- otherwise labels arrive empty ("-").

USAGE  (run from the dataset repo folder, the one with training/ and testing/)
    edge-impulse-uploader --clean        # log in + pick your project (once)
    python upload_rps.py
  or non-interactive:
    python upload_rps.py --api-key ei_xxx
  or from anywhere:
    python upload_rps.py --dataset /path/to/kaust-dsa299-rps-dataset

Expected counts: training rock 740 / paper 553 / scissors 584;
                 testing  rock 181 / paper 162 / scissors 127.
("already exists" lines are duplicates EI skips by hash -- not errors.)
"""

import argparse
import glob
import os
import subprocess
import sys

CLASSES = ["rock", "paper", "scissors"]
SPLITS = ["training", "testing"]

# Keep each command line safely under cmd.exe's ~8191-char limit on Windows.
# Other shells allow far more, so the cap only really matters on Windows.
MAX_CMDLINE = 7000 if os.name == "nt" else 120000


def find_dataset(explicit):
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (explicit, os.getcwd(), here):
        if cand and os.path.isdir(os.path.join(cand, "training")) \
                and os.path.isdir(os.path.join(cand, "testing")):
            return cand
    sys.exit("Could not find training/ and testing/ folders.\n"
             "Run this from the dataset repo, or pass --dataset PATH.")


def length_batches(files, base_len, cap):
    """Yield batches whose rendered command line stays under `cap` chars."""
    batch, cur = [], base_len
    for f in files:
        add = len(f) + 3  # quotes + separator
        if batch and cur + add > cap:
            yield batch
            batch, cur = [], base_len
        batch.append(f)
        cur += add
    if batch:
        yield batch


def run_uploader(args_list):
    full = ["edge-impulse-uploader"] + args_list
    try:
        if os.name == "nt":
            # Run via cmd.exe (needed for the .cmd shim) with a properly quoted STRING.
            return subprocess.run(subprocess.list2cmdline(full), shell=True).returncode
        return subprocess.run(full).returncode
    except FileNotFoundError:
        sys.exit("edge-impulse-uploader not found. Install it:\n"
                 "    npm install -g edge-impulse-cli")


def main():
    ap = argparse.ArgumentParser(description="Upload the RPS dataset to Edge Impulse.")
    ap.add_argument("--dataset", help="path to the dataset repo (default: current folder)")
    ap.add_argument("--api-key", help="EI API key (else uses your cached `--clean` login)")
    ap.add_argument("--max-chars", type=int, default=MAX_CMDLINE,
                    help=f"max command-line length per call (default {MAX_CMDLINE})")
    args = ap.parse_args()

    base = find_dataset(args.dataset)
    print(f"Dataset: {base}")

    grand_total = 0
    for split in SPLITS:
        for cls in CLASSES:
            files = sorted(glob.glob(os.path.join(base, split, cls, "*.jpg")))
            if not files:
                print(f"[skip] {split}/{cls}: no .jpg found")
                continue
            fixed = ["--category", split, "--label", cls]
            if args.api_key:
                fixed += ["--api-key", args.api_key]
            base_len = len(subprocess.list2cmdline(["edge-impulse-uploader"] + fixed)) + 1
            batches = list(length_batches(files, base_len, args.max_chars))
            print(f"[{split}/{cls}] {len(files)} files in {len(batches)} batch(es)...")
            for bi, batch in enumerate(batches, 1):
                rc = run_uploader(fixed + batch)
                if rc != 0:
                    print(f"  note: {split}/{cls} batch {bi}/{len(batches)} returned {rc} "
                          f"(usually duplicates already in the project -- safe to ignore).")
            grand_total += len(files)

    print(f"\nDone. Submitted {grand_total} files.")
    print("Verify in Studio -> Data acquisition:")
    print("  training  rock 740 | paper 553 | scissors 584")
    print("  testing   rock 181 | paper 162 | scissors 127")


if __name__ == "__main__":
    main()
