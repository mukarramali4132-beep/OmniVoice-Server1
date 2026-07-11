class OmniVoiceError(Exception):
    """
    Base exception for the server.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ):

        self.message = message
        self.status_code = status_code

        super().__init__(message)


# ---------------------------------------------------------


class ReferenceAudioNotFoundError(OmniVoiceError):

    def __init__(
        self,
        path: str,
    ):

        super().__init__(
            message=f"Reference audio not found: {path}",
            status_code=404,
        )


# ---------------------------------------------------------


class ModelNotLoadedError(OmniVoiceError):

    def __init__(self):

        super().__init__(
            message="OmniVoice model is not loaded.",
            status_code=503,
        )


# ---------------------------------------------------------


class GenerationFailedError(OmniVoiceError):

    def __init__(
        self,
        message="Voice generation failed.",
    ):

        super().__init__(
            message=message,
            status_code=500,
        )