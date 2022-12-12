import base64

from django.db.models.fields.files import FieldFile


def file_to_base64(file: FieldFile) -> str:
    """
    Converts file(an image or just file) to base64

    :param file: FieldFile instance or an ancestor of FieldFile
    :return: base64 representation of the file
    """
    try:
        with file.open("rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        raise OSError("Error encoding file")
