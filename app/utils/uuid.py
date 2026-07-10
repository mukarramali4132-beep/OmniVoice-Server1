import uuid


def uuid_filename(
    extension: str = ".wav",
) -> str:

    return (
        f"{uuid.uuid4().hex}{extension}"
    )