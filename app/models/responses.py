from pydantic import BaseModel


class CloneResponse(BaseModel):

    success: bool

    filename: str

    path: str

    duration: float

    sampling_rate: int