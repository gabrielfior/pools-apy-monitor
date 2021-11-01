import requests

from db.Platforms import StatsUrls
import js2py


class BeefyFetcher:
    def __init__(self, apy_url=StatsUrls.BEEFY_FINANCE_APY.value,
                 lp_url=StatsUrls.BEEFY_FINANCE_LP.value,
                 pool_addresses_url=StatsUrls.BEEFY_FINANCE_POOL_ADDRESSES.value):
        self.apy_url = apy_url
        self.lp_url = lp_url
        self.pool_addresses_url = pool_addresses_url

    def fetch_daily_stats(self):
        apys = requests.get(self.apy_url).json()
        lp_json = requests.get(self.lp_url).json()
        pool_addresses = self.fetch_pool_addresses()

        return apys, lp_json, pool_addresses

    def fetch_pool_addresses(self):
        pool_id_to_address = {}

        # fetch pools
        r = requests.get(self.pool_addresses_url)

        pool_js = js2py.eval_js(r.text.replace('export', ''))

        for jdict in pool_js:
            # in most cases id == oracleId, however for some strange cases oracleId
            # should be used for matching APYs and/or LPs.
            pool_id = jdict['oracleId']
            address = jdict['earnContractAddress']
            pool_id_to_address[pool_id] = address

        return pool_id_to_address
