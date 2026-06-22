# KAUST DSA-299 — Rock-Paper-Scissors dataset (image classification)

A cleaned **image-classification** dataset of real hands for the Edge ML (TinyML) course's
**Vision_RPS** project. Three classes — `rock`, `paper`, `scissors` — already split into
`training/` and `testing/`, ready to upload to Edge Impulse.

```
training/  rock/ paper/ scissors/      # 1,877 images
testing/   rock/ paper/ scissors/      #   470 images
```

| split | rock | paper | scissors | total |
|---|---|---|---|---|
| training | 740 | 553 | 584 | 1877 |
| testing | 181 | 162 | 127 | 470 |

≈80/20 split. Images are JPEG, square-ish crops centered on a single hand (so they fit a
96×96 RGB impulse without distortion). Each file is named **`<class>.<original>.jpg`**
(e.g. `rock.0001_….jpg`) so Edge Impulse can **infer the label from the filename**.

**Leakage-safe split.** Many source images are frames sampled from the same videos. The
train/test split is **grouped by source clip** — every frame of a given clip is in *one*
split only — so the test accuracy isn't inflated by near-duplicate frames. To reduce that
redundancy, each source clip is also **capped at 60 images** (sharpest kept).

## How to load it into Edge Impulse (CLI)

This is the course's **third data-ingestion method** (Day 1 motion = CLI data-forwarder,
KWS = Studio web upload, RPS = repo + CLI uploader). Install the Edge Impulse CLI first
(see the course `Prerequisites_Setup_Guide.md`).

**First, in Studio:** create the project and set **Dashboard → Labeling method → "One label
per data item"** (image classification). If it's left on *object detection* (bounding boxes),
uploads arrive **unlabeled (`-`)**.

**Then upload** with the cross-platform helper (works on Windows / macOS / Linux — it globs
the files and uploads in chunks):

```bash
git clone <this-repo-url>
cd kaust-dsa299-rps-dataset

edge-impulse-uploader --clean        # log in + pick your project (once)
python upload_rps.py                  # uploads all 6 class folders, labeled
```

Confirm in **Studio → Data acquisition** that all three classes appear in both Training and
Testing, with counts matching the table above.

> ⚠️ **Don't use `--directory`** — the uploader (v1.39.x) can't parse the nested
> `training/testing ÷ class` layout (`EISDIR` at the repo root, "format not recognised" at a
> split). **Don't rely on Studio's web drag-and-drop** for the full set either — it can
> silently drop files on large batches. The helper is the reliable, complete path.
>
> *macOS/Linux/Git-Bash only:* the shell expands globs, so you can instead run six
> `edge-impulse-uploader --category <split> --label <class> <split>/<class>/*.jpg` commands.
> (Windows cmd/PowerShell don't expand `*.jpg`, which is why the helper exists.)

## How this dataset was built

1. **Source:** "Rock Paper Scissors SXSW" — a real-hands, varied-background **object-detection**
   dataset from Roboflow Universe (see `ATTRIBUTION.md`).
2. **Crop → classification:** each labeled bounding box was cropped into its own per-class
   image (square, +15% context margin) so a *detection* dataset becomes a *classification*
   dataset.
3. **Quality clean:** crops were scored for sharpness (variance-of-Laplacian) and size; the
   blurriest/smallest ~12% (sharpness < 60 or min-dimension < 90 px) were removed.
4. **Dedup + leakage-safe split:** each source clip was capped at 60 images (sharpest kept)
   to cut near-duplicate frames, then split ~80/20 **grouped by source clip** so no clip
   appears in both train and test.

The reproducible scripts live in the course repo under `Projects/Vision_RPS/Dataset/`
(`crop_boxes_to_classification.py`, `quality_audit.py`, `apply_cleaning.py`,
`resplit_dedup.py`).

## Known limitation (a teaching point)

These are varied real-world hands, but the camera/lighting differs from the XIAO's. If live
accuracy is weak, **close the domain gap**: capture ~20–40 real classroom hands per class
with the XIAO (`Arduino/XIAO_ESP32S3/02_capture`), add them to your project, and retrain.
This is Day 5, Session 4.

## License

**CDLA-Sharing-1.0** (Community Data License Agreement – Sharing, Version 1.0) — see
`LICENSE`. This is a **derived/cleaned** version of the CDLA-Sharing-licensed
"Rock Paper Scissors SXSW" dataset, so it's published under the **same** share-alike
Agreement. Free to use (including commercially) and re-publish, provided you keep the
attribution (`ATTRIBUTION.md`) and change notice (`NOTICE.md`), include the `LICENSE` text,
and publish any further changes under CDLA-Sharing-1.0. See `ATTRIBUTION.md` for source
credit and `NOTICE.md` for exactly what was changed.

`SPDX-License-Identifier: CDLA-Sharing-1.0`
