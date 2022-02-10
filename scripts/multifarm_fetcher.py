import datetime

import requests

from db.Platforms import StatsUrls
import js2py

from db.write_to_table import APYWrapper


class MultifarmFetcher:
    def __init__(self, apy_url=StatsUrls.MULTIFARM_ANCHOR_APY.value):
        self.apy_url = apy_url

    def fetch_daily_stats(self):
        farm_info = requests.get(self.apy_url).json()
        return farm_info