from pydantic import BaseModel


class HealthResponse(BaseModel):

    status: str

    server: str

    version: str