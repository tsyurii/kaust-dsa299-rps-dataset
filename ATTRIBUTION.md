# Attribution

This dataset is a **derived work** ("Enhanced Data" under CDLA-Sharing-1.0).

## Source dataset

- **Name:** Rock Paper Scissors (SXSW) — hand-gesture detection
- **Provider:** Roboflow Universe (Team Roboflow / community project)
- **License:** **Community Data License Agreement – Sharing, Version 1.0
  (`CDLA-Sharing-1.0`)** — https://cdla.dev/sharing-1-0/
- **Type:** object detection (bounding boxes around rock/paper/scissors hands)
- **Links:**
  - https://universe.roboflow.com/roboflow-58fyf/rock-paper-scissors-sxsw
  - https://universe.roboflow.com/team-roboflow/rock-paper-scissors-detection
  - Download mirror used: https://www.kaggle.com/datasets/adilshamim8/rock-paper-scissors

> Credit and links to the original Data Provider(s) are preserved here as required by
> CDLA-Sharing-1.0 §3.1(c). If the source page lists specific contributor names, add them
> to this section.

## Modifications made (see `NOTICE.md` for the prominent change notice)

- Cropped each annotated bounding box into a separate per-class image (square, +15% margin).
- Converted the object-detection labels into image-classification folders
  (`rock`/`paper`/`scissors`).
- Removed low-quality crops (blur/too-small) via an automated sharpness + size filter.
- Re-organized into `training/` and `testing/`.

## License of THIS dataset

Because the source is **CDLA-Sharing-1.0** (share-alike), this derived dataset is **also
published under CDLA-Sharing-1.0** — see `LICENSE`. You may use it (including commercially)
and re-publish it, provided you keep this attribution + `NOTICE.md`, include the `LICENSE`
text, publish under the same Agreement, and flag any further changes you make.
