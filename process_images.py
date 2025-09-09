"""Script para redimensionar imágenes a 28x28 en escala de grises.

Uso básico:
    python process_images.py --input . --output procesadas

Requisitos: pip install -r requirements.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from PIL import Image


def collect_images(input_dir: Path, patterns: Iterable[str] = ("*.jpg", "*.jpeg", "*.png", "*.bmp")) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(input_dir.glob(pattern))
    # Eliminar duplicados preservando orden
    seen = set()
    unique: list[Path] = []
    for f in files:
        if f not in seen and f.is_file():
            seen.add(f)
            unique.append(f)
    return unique


def process_image(src: Path, dst: Path, size: int) -> None:
    with Image.open(src) as img:
        img = img.convert("L").resize((size, size), Image.Resampling.LANCZOS)
        img.save(dst)


def main() -> None:
    parser = argparse.ArgumentParser(description="Redimensiona imágenes a NxN y las convierte a escala de grises.")
    parser.add_argument("--input", "-i", type=Path, default=Path("."), help="Carpeta de entrada (por defecto el directorio actual)")
    parser.add_argument("--output", "-o", type=Path, default=Path("procesadas"), help="Carpeta de salida")
    parser.add_argument("--size", "-s", type=int, default=28, help="Tamaño (ancho=alto) destino en píxeles (default=28)")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescribir si ya existe el archivo destino")
    args = parser.parse_args()

    input_dir: Path = args.input
    output_dir: Path = args.output
    size: int = args.size

    if size <= 0:
        raise SystemExit("--size debe ser > 0")

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Directorio de entrada no válido: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    images = collect_images(input_dir)
    if not images:
        print("No se encontraron imágenes para procesar.")
        return

    print(f"Procesando {len(images)} imágenes -> {output_dir} (tamaño {size}x{size})")
    processed = 0
    skipped = 0
    for img_path in images:
        dst = output_dir / img_path.name
        if dst.exists() and not args.overwrite:
            skipped += 1
            continue
        try:
            process_image(img_path, dst, size)
            processed += 1
        except Exception as e:  # noqa: BLE001
            print(f"Error procesando {img_path.name}: {e}")
    print(f"Listo. Procesadas: {processed}. Omitidas: {skipped}.")


if __name__ == "__main__":  # pragma: no cover
    main()
