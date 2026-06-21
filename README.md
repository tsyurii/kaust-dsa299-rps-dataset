# KAUST DSA-299 — Rock-Paper-Scissors dataset (image classification)

A cleaned **image-classification** dataset of real hands for the Edge ML (TinyML) course's
**Vision_RPS** project. Three classes — `rock`, `paper`, `scissors` — already split into
`training/` and `testing/`, ready to upload to Edge Impulse.

```
training/  rock/ paper/ scissors/      # 4,051 images
testing/   rock/ paper/ scissors/      #   190 images
```

| split | rock | paper | scissors |
|---|---|---|---|
| training | 1708 | 1171 | 1172 |
| testing | 63 | 65 | 62 |

Images are JPEG, square-ish crops centered on a single hand (so they fit a 96×96 RGB impulse
without distortion).

## How to load it into Edge Impulse (CLI)

This is the course's **third data-ingestion method** (Day 1 motion = CLI data-forwarder,
KWS = Studio web upload, RPS = repo + CLI uploader). Install the Edge Impulse CLI first
(see the course `Prerequisites_Setup_Guide.md`), then:

```bash
git clone <this-repo-url>
cd kaust-dsa299-rps-dataset

edge-impulse-uploader --api-key ei_xxxxxxxx          # key: Studio → Dashboard → Keys
edge-impulse-uploader --category training --directory training
edge-impulse-uploader --category testing  --directory testing
```

Labels are inferred from the folder names (`rock`/`paper`/`scissors`); uploading each split
with `--category` preserves the train/test split. Confirm in **Studio → Data acquisition**
that all three classes appear in both Training and Testing.

## How this dataset was built

1. **Source:** "Rock Paper Scissors SXSW" — a real-hands, varied-background **object-detection**
   dataset from Roboflow Universe (see `ATTRIBUTION.md`).
2. **Crop → classification:** each labeled bounding box was cropped into its own per-class
   image (square, +15% context margin) so a *detection* dataset becomes a *classification*
   dataset.
3. **Quality clean:** crops were scored for sharpness (variance-of-Laplacian) and size; the
   blurriest/smallest ~12% (sharpness < 60 or min-dimension < 90 px) were removed. The
   reproducible scripts live in the course repo under
   `Projects/Vision_RPS/Dataset/` (`crop_boxes_to_classification.py`, `quality_audit.py`,
   `apply_cleaning.py`).

## Known limitation (a teaching point)

These are varied real-world hands, but the camera/lighting differs from the XIAO's. If live
accuracy is weak, **close the domain gap**: capture ~20–40 real classroom hands per class
with the XIAO (`Arduino/XIAO_ESP32S3/02_capture`), add them to your project, and retrain.
This is Day 5, Session 4.

## License

Derived work; see `ATTRIBUTION.md` for the source dataset's license and credit.
