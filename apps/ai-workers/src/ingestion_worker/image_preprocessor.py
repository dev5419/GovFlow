"""
GovFlow Image Preprocessor
Uses OpenCV and Pillow (locked per techstack.md) for deskewing, scaling,
and contrast adjustment on scanned document images before OCR extraction.
"""

import io
import os
from dataclasses import dataclass
from typing import Tuple

import cv2
import numpy as np
from PIL import Image


@dataclass
class PreprocessedImage:
    """Preprocessed image artifact."""
    image_bytes: bytes
    width: int
    height: int
    format: str
    skew_angle_deg: float


def _deskew_image(cv_img: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Detect text skew angle and rotate image straight using OpenCV contours & minAreaRect.
    """
    # Convert to grayscale
    if len(cv_img.shape) == 3:
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    else:
        gray = cv_img

    # Invert and threshold to isolate text features
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Find all foreground coordinates
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 100:
        return cv_img, 0.0

    # Find minimum bounding box around text pixels
    rect = cv2.minAreaRect(coords)
    angle = rect[-1]

    # OpenCV minAreaRect returns angle in [-90, 0)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Only apply rotation if significant skew detected (> 0.5 degrees and < 45 degrees)
    if 0.5 < abs(angle) < 45.0:
        (h, w) = cv_img.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            cv_img,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )
        return rotated, float(angle)

    return cv_img, 0.0


def _enhance_contrast(cv_img: np.ndarray) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE) for scanned document legibility.
    """
    if len(cv_img.shape) == 3:
        # Convert to LAB color space and equalize L channel
        lab = cv2.cvtColor(cv_img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(cv_img)


def _normalize_scale(cv_img: np.ndarray, max_dim: int = 2400) -> np.ndarray:
    """
    Scale image so maximum dimension does not exceed max_dim, preserving aspect ratio.
    """
    h, w = cv_img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        new_w = int(round(w * scale))
        new_h = int(round(h * scale))
        return cv2.resize(cv_img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return cv_img


def preprocess_image(
    image_source: bytes | io.BytesIO | str | np.ndarray,
    target_format: str = "PNG",
) -> PreprocessedImage:
    """
    Preprocesses a scanned or digital document image:
    1. Deskews text orientation
    2. Enhances contrast using CLAHE
    3. Normalizes scale and dimensions
    4. Encodes to clean output bytes
    """
    # Load into OpenCV numpy array
    if isinstance(image_source, np.ndarray):
        cv_img = image_source
    elif isinstance(image_source, bytes):
        nparr = np.frombuffer(image_source, np.uint8)
        cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(image_source, io.BytesIO):
        nparr = np.frombuffer(image_source.getvalue(), np.uint8)
        cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    elif isinstance(image_source, str):
        if not os.path.isfile(image_source):
            raise FileNotFoundError(f"Image file not found: {image_source}")
        cv_img = cv2.imread(image_source, cv2.IMREAD_COLOR)
    else:
        raise ValueError("Unsupported image source type.")

    if cv_img is None:
        raise ValueError("Failed to decode image.")

    # 1. Deskew
    deskewed_img, skew_angle = _deskew_image(cv_img)

    # 2. Contrast adjustment
    enhanced_img = _enhance_contrast(deskewed_img)

    # 3. Scaling / resolution normalization
    scaled_img = _normalize_scale(enhanced_img)

    h, w = scaled_img.shape[:2]

    # Convert back to PIL for clean encoding
    if len(scaled_img.shape) == 3:
        rgb_img = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2RGB)
    else:
        rgb_img = scaled_img

    pil_img = Image.fromarray(rgb_img)
    buffer = io.BytesIO()
    fmt = target_format.upper()
    if fmt in ("JPG", "JPEG"):
        pil_img.save(buffer, format="JPEG", quality=95)
    else:
        pil_img.save(buffer, format="PNG", optimize=True)

    return PreprocessedImage(
        image_bytes=buffer.getvalue(),
        width=w,
        height=h,
        format=fmt,
        skew_angle_deg=skew_angle,
    )
