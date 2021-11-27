import requests

from db.Platforms import StatsUrls
import js2py


class BeefyFetcher:
    def __init__(self, apy_url=StatsUrls.BEEFY_FINANCE_APY.value,
                 lp_url=StatsUrls.BEEFY_FINANCE_LP.value,
                 pool_addresses_chain_ids=[('polygon',StatsUrls.BEEFY_FINANCE_POLYGON_POOL_ADDRESS.value),
                                            ('celo',StatsUrls.BEEFY_FINANCE_CELO_POOL_ADDRESS.value),
                                            ('bsc', StatsUrls.BEEFY_FINANCE_BSC_POOL_ADDRESS.value)]):
        self.apy_url = apy_url
        self.lp_url = lp_url
        self.pool_addresses_chain_ids = pool_addresses_chain_ids

    def fetch_daily_stats(self):
        apys = requests.get(self.apy_url).json()
        lp_json = requests.get(self.lp_url).json()
        pool_addresses_and_chain = self.fetch_pool_addresses()

        return apys, lp_json, pool_addresses_and_chain

    def fetch_pool_addresses(self):
        pool_id_to_address_and_chain = {}

        # fetch pools
        for chain_name, pool_address in self.pool_addresses_chain_ids:
            print ('reading from {}'.format(pool_address))

            r = requests.get(pool_address)
            pool_js = js2py.eval_js(r.text.replace('export', ''))

            for jdict in pool_js:
                # we store the same address under both IDs for later mapping.
                address = jdict['earnContractAddress']
                pool_id_to_address_and_chain[jdict['id']] = (chain_name, address)
                pool_id_to_address_and_chain[jdict['oracleId']] = (chain_name, address)

        return pool_id_to_address_and_chain
