import os
import uuid
from typing import Optional

from PIL import Image


def convert_image_to_pdf(image_path: str, temp_dir: Optional[str] = None) -> str:
    """
    Converte JPG/PNG/etc para um PDF temporário na mesma pasta (ou numa pasta temp).
    Retorna o caminho do PDF gerado.
    """
    if temp_dir is None:
        temp_dir = os.path.dirname(image_path)

    os.makedirs(temp_dir, exist_ok=True)

    img = Image.open(image_path).convert("RGB")

    temp_filename = f"__temp_{uuid.uuid4().hex}.pdf"
    temp_path = os.path.join(temp_dir, temp_filename)

    img.save(temp_path, "PDF", resolution=100.0)
    return temp_path
