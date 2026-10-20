from worker import config


class FlashHeadAvatarServer:
    """Loads FlashHead once on the GPU; turns incoming speech audio into frames and publishes audio + video together."""

    def __init__(self):
        self.model_variant = config.AVATAR_MODEL_VARIANT
        self.reference_image_path = config.AVATAR_REFERENCE_IMAGE_PATH
        self.frame_rate = config.AVATAR_FRAME_RATE
        self.host = config.AVATAR_SERVER_HOST
        self.port = config.AVATAR_SERVER_PORT

    def run(self):
        raise NotImplementedError

    def clear_playback(self):
        """Drops queued audio and frames on interruption and returns to the idle face."""
        raise NotImplementedError
