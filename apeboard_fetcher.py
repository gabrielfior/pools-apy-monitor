import requests
from aux_classes import PoolBalanceHolder
from base_fetcher import BaseFetcher

class ApeboardFetcher(BaseFetcher):
    def __init__(self, account_holder) -> None:
        self.account_holder = account_holder

    def fetch_data(self):
        return self.fetch_polygon_pools() + self.fetch_bsc_pools() + self.fetch_terra_pools() + self.fetch_solana_pools()

    def fetch_bsc_pools(self):

        if not self.account_holder.account_bsc:
            return []

        headers = self.build_headers()
        response = requests.get('https://api.apeboard.finance/pancakeswapBsc/{}'.format(self.account_holder.account_bsc), headers=headers)
        pool_balances = []
        reward_dict = {}
        for v in response.json()['vaults']:
            for reward in v['rewards']:
                reward_dict[reward['address']] = {'price': reward['price'], 'balance': reward['balance']}
            for token in v['tokens']:
                p = PoolBalanceHolder(token['symbol'],token['address'], token['balance'], 
                float(token['price']), token['balance']*float(token['price']))
                if p.address in reward_dict:
                    # add rewards
                    reward = reward_dict[p.address]
                    p.balance += reward['balance']
                    p.value_usd += reward['balance']*reward['price']
                pool_balances.append(p)
        
        return pool_balances

    def fetch_polygon_pools(self):

        if not self.account_holder.account_polygon:
            return []

        headers = self.build_headers()
        response = requests.get('https://api.apeboard.finance/beefyPolygon/{}'.format(self.account_holder.account_polygon), headers=headers)
        data = response.json()
        pool_balances = []
        for pos in data['positions']:
            for token in pos['tokens']:
                pool_balances.append(PoolBalanceHolder(token['symbol'], token['address'], token['balance'],
                float(token['price']), token['balance']*float(token['price'])))

        return pool_balances

    def fetch_terra_pools(self):

        if not self.account_holder.account_terra:
            return []

        headers = self.build_headers()
        response = requests.get('https://api.apeboard.finance/apollodaoTerra/{}'.format(self.account_holder.account_terra), headers=headers)
        data = response.json()
        pool_balances = []
        for farm in data['farms']:
            farm_address = farm['lpAddress']
            lp_balance = farm['balance']
            total_usd = 0.
            for token in farm['tokens']:
                # we sum up the rewards for each side of the pool i.e. token
                total_usd += token['balance'] * token['price']
            # lp_price not populated by the API
            lp_price = total_usd/lp_balance
            pool_balances.append(PoolBalanceHolder('terra-farm-XX',farm_address, lp_balance, 
                                lp_price, total_usd))

        return pool_balances

    def fetch_solana_pools(self):

        if not self.account_holder.account_solana:
            return []

        headers = self.build_headers()
        response = requests.get('https://api.apeboard.finance/solfarmSolana/{}'.format(self.account_holder.account_solana), headers=headers)
        data = response.json()
        pool_balances = []
        for position in data['positions']:
            farm_address = None
            total_usd = 0.
            lp_balance = position['balance']
            for token in position['tokens']:
                # we sum up the rewards for each side of the pool i.e. token
                total_usd += token['balance'] * token['price']
            # lp_price not populated by the API
            lp_price = total_usd/lp_balance
            pool_balances.append(PoolBalanceHolder('solana-farm-XX',farm_address, lp_balance, 
                                lp_price, total_usd))
        return pool_balances
