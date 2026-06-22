#!/usr/bin/env python3
"""
upload_rps.py — upload the Rock-Paper-Scissors dataset to Edge Impulse.

Cross-platform (Windows / macOS / Linux). Solves the two things that bite the bare
`edge-impulse-uploader ... *.jpg` command:
  * Windows cmd/PowerShell don't expand `*.jpg` -> Python globs the files itself.
  * Huge file lists blow past the OS command-line length limit -> uploads in chunks.

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


def find_dataset(explicit):
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (explicit, os.getcwd(), here):
        if cand and os.path.isdir(os.path.join(cand, "training")) \
                and os.path.isdir(os.path.join(cand, "testing")):
            return cand
    sys.exit("Could not find training/ and testing/ folders.\n"
             "Run this from the dataset repo, or pass --dataset PATH.")


def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def run_uploader(args_list):
    # On Windows the CLI is edge-impulse-uploader.cmd -> needs the shell to resolve it.
    cmd = ["edge-impulse-uploader"] + args_list
    try:
        return subprocess.run(cmd, shell=(os.name == "nt")).returncode
    except FileNotFoundError:
        sys.exit("edge-impulse-uploader not found. Install it:\n"
                 "    npm install -g edge-impulse-cli")


def main():
    ap = argparse.ArgumentParser(description="Upload the RPS dataset to Edge Impulse.")
    ap.add_argument("--dataset", help="path to the dataset repo (default: current folder)")
    ap.add_argument("--api-key", help="EI API key (else uses your cached `--clean` login)")
    ap.add_argument("--chunk", type=int, default=100, help="files per upload call (default 100)")
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
            print(f"[{split}/{cls}] uploading {len(files)} files...")
            for batch in chunks(files, args.chunk):
                call = ["--category", split, "--label", cls]
                if args.api_key:
                    call += ["--api-key", args.api_key]
                call += batch
                rc = run_uploader(call)
                if rc != 0:
                    print(f"  note: a batch in {split}/{cls} returned {rc} "
                          f"(usually duplicates already in the project -- safe to ignore).")
            grand_total += len(files)

    print(f"\nDone. Submitted {grand_total} files.")
    print("Verify in Studio -> Data acquisition:")
    print("  training  rock 740 | paper 553 | scissors 584")
    print("  testing   rock 181 | paper 162 | scissors 127")


if __name__ == "__main__":
    main()
