import requests

from db.Platforms import StatsUrls


class MultifarmFetcher:
    # ToDo - Check if APYs match platform's APYs (Anchor did not, diff 2%)
    def __init__(self, apy_url=StatsUrls.MULTIFARM_ANCHOR_APY.value):
        self.apy_url = apy_url

    def fetch_daily_stats(self):
        farm_info = requests.get(self.apy_url).json()
        return farm_info