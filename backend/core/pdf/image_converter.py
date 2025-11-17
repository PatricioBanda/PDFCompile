import os
from PIL import Image
import uuid

def convert_image_to_pdf(image_path):
    """
    Converte JPG/PNG/etc para um PDF temporário.
    """
    img = Image.open(image_path).convert("RGB")
    temp_path = os.path.join(
        os.path.dirname(image_path),
        f"__temp_{uuid.uuid4().hex}.pdf"
    )
    img.save(temp_path, "PDF", resolution=100.0)
    return temp_path
