# BNL-AI — Rodent Pose Estimation Pipeline

**Behavioural Neuroscience Laboratory**

A two-stage deep learning pipeline for markerless pose estimation in laboratory rodents. The system first detects the animal with **YOLOv11**, then predicts body-part keypoints using **HRNet-W48**, enabling automated behavioural analysis from standard cage-mounted cameras.

---

## Demo Results

### Pose Predictions (Bottom View, Confidence = 1.0)

<img width="640" height="360" alt="R1_mike_20250311_170_1_V01_168" src="https://github.com/user-attachments/assets/f05d1271-1129-4898-85b1-9a4ba8c265ff" />

<img width="620" height="360" alt="R1_mike_20250311_170_1_V01_914" src="https://github.com/user-attachments/assets/6e5f9807-f2b3-43d0-b000-bbdde12c7408" />

<img width="620" height="360" alt="R1_mike_20250311_180_1_V01_709" src="https://github.com/user-attachments/assets/175ee38a-a782-4945-8365-5d2e487a2ddf" />

### Prediction vs Ground Truth (Test Set)

<img width="850" height="850" alt="32" src="https://github.com/user-attachments/assets/95514366-4e36-4d42-8661-d782bee2e4e4" />

<img width="850" height="850" alt="15" src="https://github.com/user-attachments/assets/ce3a11b9-6d85-4170-b6f1-12677b1db9c2" />

<img width="850" height="850" alt="12" src="https://github.com/user-attachments/assets/a87ac94b-6ca1-4e40-9a1a-7b43985d9ecf" />

### Detection Examples (Train / Val / Test)

<img width="400" height="300" alt="detection batches" src="https://github.com/user-attachments/assets/19a068f6-8c16-459f-a25e-4d8a569591c5" />

---

## Pipeline Overview

```
Video / Image
     │
     ▼
┌──────────────┐
│  YOLOv11     │  →  Bounding box around the rodent
│  (Detection) │
└──────┬───────┘
       │  Crop + Pad + Resize
       ▼
┌──────────────┐
│  HRNet-W48   │  →  Per-keypoint heatmaps
│  (Pose)      │
└──────┬───────┘
       │  Argmax + Confidence filter
       ▼
  Keypoint coordinates (up to 35 body parts)
```

The pipeline supports up to **35 keypoints** (top view) or **14 keypoints** (bottom view), covering ears, eyes, nose, spine, limbs, and tail landmarks. Predictions are exported as annotated videos and per-frame CSV files.

---

## Repository Structure

```
bnl-ai/
├── hrnet.py                 # HRNet-W48 pose estimation model (Microsoft)
├── resnet.py                # ResNet-based pose estimation model
├── SHG.py                   # Stacked Hourglass pose estimation model
├── PoseDataset.py           # PyTorch Dataset with augmentation & heatmap generation
├── train_pose.py            # Training loop (Adam + ReduceLROnPlateau)
├── train_detection.py       # YOLOv11 fine-tuning for rodent detection
├── test_pose.py             # Evaluation: RMSE, coverage, per-keypoint metrics
├── predict_pose.py          # Batch image inference → CVAT-compatible annotations
├── predict_detection.py     # YOLOv11 detection inference
├── infer_video.py           # Full video inference (detection + pose)
├── plotlosses.py            # Training curve visualization
├── conversion.py            # MKV → MP4 batch converter (ffmpeg)
├── installation.sh          # Dependency installation script
├── slurm-script.sh          # SLURM job submission for HPC clusters
├── config/                  # HRNet YAML configs (w48_256x192, w48_384x288)
├── conversion_scripts/
│   ├── script_cvat_xml_to_csv.py    # CVAT XML annotations → CSV
│   ├── script_merge_csv_files.py    # Merge multiple annotation CSVs
│   ├── convert_csv_to_h5.py         # CSV → HDF5 (DeepLabCut format)
│   └── frame extraction.m           # MATLAB frame extraction from video
├── trained_models/          # Saved model checkpoints
├── out/                     # Training outputs, test images, loss CSVs
└── tools/
    └── plot_losses.py       # Loss plotting utility
```

---

## Installation

```bash
# Core dependencies
pip install pyyaml numpy pandas matplotlib alive-progress opencv-python ultralytics pillow scikit-learn termcolor

# PyTorch with CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## Usage

### Train Detection Model

```bash
python train_detection.py
```

Fine-tunes YOLOv11 on labelled rodent bounding boxes (YOLO format dataset with `config.yaml`).

### Train Pose Estimation Model

```bash
python train_pose.py
```

Trains HRNet-W48 on heatmap regression with MSE loss. Supports configurable learning rate scheduling (Adam + ReduceLROnPlateau), data augmentation (rotation, scaling, horizontal flip, color jitter), and automatic early stopping. The best checkpoint is saved based on validation loss.

### Run on HPC (SLURM)

```bash
sbatch slurm-script.sh
```

### Evaluate on Test Set

```bash
python test_pose.py
```

Computes RMSE and coverage per keypoint across configurable confidence thresholds. Generates side-by-side prediction vs ground truth visualizations.

### Inference on Video

```bash
python infer_video.py <path_to_video.mp4>
```

Produces an annotated video with overlaid keypoints and a CSV with per-frame coordinates and bounding boxes.

### Batch Image Inference

```bash
python predict_pose.py -i <image_folder_or_file> [-r]
```

Runs detection + pose on images and exports predictions in CVAT-importable format (JSON + manifest) for annotation correction workflows.

---

## Data Augmentation

The `PoseDataset` class applies the following augmentations during training, with consistent transforms applied to both images and keypoints:

- Random scaling (0.9×–1.1×)
- Random rotation (0°, 90°, 180°, 270°)
- Horizontal flip with automatic left/right keypoint swapping
- Color jitter (brightness, contrast, saturation, hue)
- Random Gaussian blur
- Random grayscale

---

## Annotation Workflow

The repo includes tools for a complete annotation pipeline:

1. **Extract frames** from video (`conversion_scripts/frame extraction.m`)
2. **Convert video formats** if needed (`conversion.py` — MKV → MP4)
3. **Run model inference** to generate pre-annotations (`predict_pose.py`)
4. **Import into CVAT** for manual correction (outputs CVAT-compatible ZIP)
5. **Export corrected annotations** from CVAT as XML
6. **Convert to CSV** (`script_cvat_xml_to_csv.py`)
7. **Merge annotation files** (`script_merge_csv_files.py`)

---

## Supported Keypoints

**(35 keypoints):** nose, left/right eye, left/right ear base, left/right ear tip, ears midpoint, head midpoint, lower jaw, throat, chest, back withers, back midpoint, back croup, front left/right shoulder, front left/right elbow, front left/right wrist, front left/right paw, back left/right hip, back left/right knee, back left/right wrist, back left/right paw, tail base, tail upper midpoint, tail midpoint, tail lower midpoint, tail end.


---

## Model Architectures

| Model | Source | Notes |
|-------|--------|-------|
| **HRNet-W48** | Sun et al. (Microsoft) | Primary model — maintains high-resolution representations throughout |
| **ResNet** | Xiao et al. (Microsoft) | Deconvolution-based upsampling head |
| **Stacked Hourglass** | Newell et al. | Recursive encoder-decoder with intermediate supervision |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

