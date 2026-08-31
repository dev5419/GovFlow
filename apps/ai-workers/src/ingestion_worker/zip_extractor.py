"""
GovFlow ZIP Archive Safe Extractor
Safely extracts ZIP bid packages while strictly guarding against Zip-Slip path traversal.
"""

import io
import os
import zipfile
from dataclasses import dataclass
from typing import List, Optional


SUPPORTED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}


class ZipExtractionError(Exception):
    """Raised when ZIP archive is corrupted or contains illegal path traversal."""
    pass


@dataclass
class ExtractedFile:
    """Represents a safely extracted document file from a ZIP archive."""
    file_name: str
    relative_path: str
    file_bytes: bytes
    file_size: int
    file_type: str
    is_supported: bool


def _is_safe_path(base_dir: str, path: str) -> bool:
    """
    Ensure the target path is strictly within base_dir (Zip-Slip defense).
    """
    abs_base = os.path.abspath(base_dir)
    abs_target = os.path.abspath(os.path.join(base_dir, path))
    return abs_target.startswith(abs_base) and not os.path.isabs(path)


def safe_extract_zip(
    zip_source: bytes | io.BytesIO | str,
    output_dir: Optional[str] = None,
) -> List[ExtractedFile]:
    """
    Safely extract files from a ZIP archive in memory or to an optional output directory.
    Guards against directory traversal (Zip-Slip), dangerous symlinks, and extracts supported files.
    """
    if isinstance(zip_source, bytes):
        zip_file = zipfile.ZipFile(io.BytesIO(zip_source))
    elif isinstance(zip_source, io.BytesIO):
        zip_file = zipfile.ZipFile(zip_source)
    elif isinstance(zip_source, str):
        if not os.path.isfile(zip_source):
            raise ZipExtractionError(f"ZIP source file not found: {zip_source}")
        zip_file = zipfile.ZipFile(zip_source)
    else:
        raise ZipExtractionError("Invalid zip_source type; expected bytes, BytesIO, or file path.")

    extracted_files: List[ExtractedFile] = []

    with zip_file:
        for member in zip_file.infolist():
            # Zip-Slip defense: check for path traversal patterns
            norm_name = os.path.normpath(member.filename)
            if norm_name.startswith("..") or os.path.isabs(norm_name) or ":" in norm_name or member.filename.startswith("../") or member.filename.startswith("..\\"):
                raise ZipExtractionError(
                    f"Illegal path traversal attempt detected in ZIP archive: '{member.filename}'"
                )

            # Skip directories and macOS / hidden metadata files
            base_name = os.path.basename(member.filename)
            if member.is_dir() or member.filename.startswith("__MACOSX/") or (base_name.startswith(".") and not base_name.startswith("..")):
                continue

            # Read file bytes directly (preserves exact original bytes)
            try:
                content = zip_file.read(member)
            except Exception as e:
                raise ZipExtractionError(f"Failed to read '{member.filename}' from ZIP: {e}")

            # Extract extension and validate
            _, ext = os.path.splitext(member.filename.lower())
            is_supported = ext in SUPPORTED_EXTENSIONS
            file_name = os.path.basename(member.filename)

            # If an output directory is specified, write safely to disk
            if output_dir:
                if not _is_safe_path(output_dir, norm_name):
                    raise ZipExtractionError(
                        f"Zip-slip path escape detected targeting: '{norm_name}'"
                    )
                dest_path = os.path.join(output_dir, norm_name)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "wb") as f:
                    f.write(content)

            extracted_files.append(
                ExtractedFile(
                    file_name=file_name,
                    relative_path=norm_name,
                    file_bytes=content,
                    file_size=len(content),
                    file_type=ext.lstrip("."),
                    is_supported=is_supported,
                )
            )

    return extracted_files
