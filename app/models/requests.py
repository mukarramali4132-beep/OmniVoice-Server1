from pydantic import BaseModel, Field


class CloneRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        description="Text to synthesize",
    )

    language: str | None = Field(
        default=None,
        description="Language code",
    )

    reference_audio: str = Field(
        ...,
        description="Reference audio path",
    )

    reference_text: str | None = Field(
        default=None,
        description="Transcript of reference audio",
    )

    speed: float | None = Field(
        default=None,
        gt=0,
    )

    duration: float | None = Field(
        default=None,
        gt=0,
    )