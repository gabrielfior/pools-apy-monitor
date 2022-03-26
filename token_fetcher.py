import requests
from aux_classes import *
from base_fetcher import BaseFetcher

class TokenFetcher(BaseFetcher):
    def __init__(self, account_network_mapper: dict) -> None:
        self.account_network_mapper = account_network_mapper
    
    def fetch_tokens(self):
        headers = self.build_headers()
        pool_balances = []
        for network, account in self.account_network_mapper.items():
            r = requests.get('https://api.apeboard.finance/wallet/{}/{}'.format(network,account), headers=headers)
            for token in r.json():
                pool_balances.append(PoolBalanceHolder(token['symbol'],token['address'], token['balance'], 
                                token['price'], token['price']*token['balance']))
        
        return pool_balances