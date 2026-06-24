import io
from uuid import UUID

from PIL import Image

from app.core.storage import S3Storage

THUMBNAIL_SIZES = {
    "large": 800,
    "medium": 400,
    "small": 150,
}


def process_image(file_bytes: bytes, media_id: UUID, property_id: UUID, content_type: str) -> dict:
    storage = S3Storage()
    base_key = f"properties/{property_id}/{media_id}"

    original_key = f"{base_key}/original.jpg"
    original_url = storage.upload_fileobj(file_bytes, original_key, content_type)

    thumbnail_urls = {}
    img = Image.open(io.BytesIO(file_bytes))
    img = img.convert("RGB")

    for name, max_size in THUMBNAIL_SIZES.items():
        thumb = img.copy()
        thumb.thumbnail((max_size, max_size), Image.LANCZOS)
        buf = io.BytesIO()
        thumb.save(buf, format="JPEG", quality=85)
        buf.seek(0)

        key = f"{base_key}/{name}.jpg"
        storage.upload_fileobj(buf.getvalue(), key, "image/jpeg")
        thumbnail_urls[name] = key

    return {
        "url": original_key,
        "thumbnail_urls": thumbnail_urls,
    }
