# NOTICE — changes to the original Data (CDLA-Sharing-1.0 §3.1(b))

**The image files in this dataset have been CHANGED from the original.** This is "Enhanced
Data" under the Community Data License Agreement – Sharing, Version 1.0 (CDLA-Sharing-1.0),
and is published under that same Agreement (see `LICENSE`).

## What was changed

Starting from the original **"Rock Paper Scissors SXSW"** object-detection dataset
(Roboflow Universe — see `ATTRIBUTION.md`), every image file here was modified as follows:

1. **Cropped** — each annotated bounding box was cut out into its own image (made square
   with a ~15% context margin), turning a detection dataset into a per-class image
   **classification** dataset (`rock` / `paper` / `scissors`).
2. **Filtered** — low-quality crops (heavy blur / very small) were removed using an
   automated sharpness (variance-of-Laplacian) + minimum-size threshold. Removed images are
   **not** included here.
3. **Re-organized** — images were placed into `training/` and `testing/` folders by class.

No pixels within a retained crop were otherwise edited. The reproducible scripts that
performed these changes live in the course repository under
`Projects/Vision_RPS/Dataset/` (`crop_boxes_to_classification.py`, `quality_audit.py`,
`apply_cleaning.py`).

## Your obligations if you re-publish

Per CDLA-Sharing-1.0: publish under the **same** Agreement, **keep this NOTICE and the
attribution** in `ATTRIBUTION.md`, include the `LICENSE` text, and add your own prominent
notice of any further changes you make.
