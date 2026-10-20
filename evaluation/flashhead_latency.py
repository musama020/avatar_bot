from worker import config


class FlashHeadLatencyTest:
    """Step 3 go/no-go: time from first audio chunk to first video frame, at several chunk sizes."""

    def __init__(self):
        self.target_first_frame_seconds = config.TARGET_AVATAR_FIRST_FRAME_SECONDS

    def run(self):
        raise NotImplementedError
