# Attribution

This dataset is a **derived work**.

## Source dataset

- **Name:** Rock Paper Scissors (SXSW) — hand-gesture detection
- **Provider:** Roboflow Universe (community/Team Roboflow project)
- **Type:** object detection (bounding boxes around rock/paper/scissors hands)
- **Links:**
  - https://universe.roboflow.com/roboflow-58fyf/rock-paper-scissors-sxsw
  - https://universe.roboflow.com/team-roboflow/rock-paper-scissors-detection
  - Kaggle mirror used for download: https://www.kaggle.com/datasets/adilshamim8/rock-paper-scissors

> ⚠️ **Verify the license on the source page before redistributing.** Roboflow Universe
> datasets are commonly licensed **CC BY 4.0** (or Public Domain) — confirm the exact terms
> shown on the project page above and record them here. Provide attribution to the original
> author(s) as required by that license.

## Modifications made for this course

- Cropped each annotated bounding box into a separate per-class image (square, +15% margin).
- Converted the object-detection labels into image-classification folders
  (`rock`/`paper`/`scissors`).
- Removed low-quality crops (blur/too-small) via an automated sharpness + size filter.

No images were otherwise altered. If the source license is share-alike (e.g. CC BY-SA),
this derived dataset must carry the same license.
