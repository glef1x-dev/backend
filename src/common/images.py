from __future__ import annotations

import pathlib

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def convert_image_to_webp_format(image: SimpleUploadedFile) -> None:
    # TODO: add some check if the SimpleUploadedFile is really an image
    Image.open(image).save(image, "webp", optimize=True, quality=95)
    image.name = pathlib.Path(image.name).with_suffix(".webp")
    image.content_type = "image/webp"
