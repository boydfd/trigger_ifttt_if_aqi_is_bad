class UserConfig:
    def __init__(self, ifttt_token, pm25_threshold=60, times=None):
        if times is None:
            times = ["7:30", "18:00"]
        self.pm25_threshold = pm25_threshold
        self.ifttt_token = ifttt_token
        self.times = times