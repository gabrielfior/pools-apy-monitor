import pdb

import requests
from pycoingecko import CoinGeckoAPI

from db.Platforms import StatsUrls


class YearnFetcher:
    network_ids = ['ethereum', 'binance-smart-chain', 'polygon-pos', 'avalanche', 'optimistic-ethereum']

    def __init__(self, url=StatsUrls.YEARN_FINANCE.value):
        self.url = url
        self.cg = CoinGeckoAPI()

    def get_network_names(self):
        platforms = self.cg.get_asset_platforms()
        d = {platform['id']: platform for platform in platforms}
        return d

    def fetch_daily_stats(self):
        apys = requests.get(self.url).json()
        return apys

    def fetch_apy_from_json(self, json_dict):
        # try extracting totalApy, if not existing netApy, else None
        if 'totalApy' in json_dict['apy']['data']:
            return  json_dict['apy']['data']['totalApy']
        elif 'netApy' in json_dict['apy']['data']:
            return json_dict['apy']['data']['netApy']
        else:
            return None

    def fetch_token_price_using_all_networks(self, address):
        # we fetch all networks, if a valid price can be returned, we return it, else None.
        for network_name in YearnFetcher.network_ids:
            price_json = self.cg.get_token_price(id=network_name, vs_currencies='usd', contract_addresses=address)
            if price_json:
                print (price_json)
                return price_json[str(address).lower()]['usd'], network_name
        return None, None
