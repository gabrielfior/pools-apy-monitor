import requests

from db.Platforms import StatsUrls


class CurveFetcher:
    def __init__(self, url=StatsUrls.POLYGON_CURVE.value):
        self.url = url

    def fetch_daily_stats_curve(self):
        r = requests.get(self.url)
        apys = r.json()['apy']['day']
        return apys
