import datetime

from brownie.network import gas_price, priority_fee, max_fee
from brownie.network.gas.strategies import LinearScalingStrategy
from brownie import Contract, accounts, Wei
import requests
from brownie import network
from scripts.token_lookup import TokenLookup, TokenDict
from dotenv import load_dotenv
from brownie import *

def get_contract_by_address(address):
    try:
        print ('trying by accessing network')
        contract = Contract(address)
    except:
        print ('trying from explorer...')
        contract = Contract.from_explorer(address)
    return contract

def main():

    print ('connecting to polygon')
    if not network.is_connected():
        network.connect('polygon-main')

    deeby_contract_address = '0x7F73CE42963fB967dF88d8815f364DCc47F1Ea89'
    
    token_lookup = TokenLookup([
        TokenDict('weth', '0x7ceb23fd6bc0add59e62ac25578270cff1b9f619', 18),
        TokenDict('wbtc', '0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6', 8),
        TokenDict('usdt', '0xc2132d05d31c914a87c6611c10748aeb04b58e8f', 6),
    ])

    deepbalancer_set_contract = get_contract_by_address(deeby_contract_address)

    # position_multiplier = 1000000.0  # usdc only
    pos = deepbalancer_set_contract.getPositions()

    r = requests.get(
        'https://api.coingecko.com/api/v3/simple/token_price/polygon-pos?contract_addresses'
        '={}&vs_currencies=usd%2Cusd&include_market_cap=false&include_24hr_vol'
        '=false&include_24hr_change=false&include_last_updated_at=false'.format(','.join(
            token_lookup.get_all_addresses()
        )))

    pos_identifiers = {}
    prices = r.json()
    set_token_value = 0.
    for pos_token in pos:
        address = pos_token[0].lower()
        token_dict = token_lookup.get_by_address(address)
        token_position = pos_token[2] / (10 ** token_dict.token_decimals)
        token_price_usd = prices[address]['usd']
        pos_identifiers[token_dict.token_name] = {
            'position': token_position,
            'price_usd': token_price_usd,
            'position_usd': token_position * token_price_usd,
        }
        set_token_value += float(token_position * token_price_usd)

    print('pos_identifier {}'.format(pos_identifiers))

    print ('token value: {}'.format(set_token_value))

    # ToDo - Check if this matches total value from TokenSets UI
    total_deepbalancer_tokens = deepbalancer_set_contract.totalSupply(
    ) / 10 ** (deepbalancer_set_contract.decimals())
    # multiply by token_price

    # Rebalance new values
    # ToDo - Get new weights from model
    deepbalancer_token_usd_value = sum([v['position_usd']
                                        for v in pos_identifiers.values()])
    curr_weights = {k: v['position_usd'] /
                       deepbalancer_token_usd_value for k, v in pos_identifiers.items()}

    total_usd_value = total_deepbalancer_tokens * deepbalancer_token_usd_value
    print('total usd value {}'.format(total_usd_value))
    print('curr weights {}'.format(curr_weights))

    if network.is_connected():
        network.disconnect()

    return  {'token_set_unit_value': set_token_value,
         'set_address': deeby_contract_address,
         'datetime_crawl': datetime.datetime.now(),
         'market_cap': total_usd_value,
         'composition_eth_btc_usdt': '-'.join(
             [str(curr_weights.get('weth', 0.0)), 
             str(curr_weights.get('wbtc',0.0)),
             str(curr_weights.get('usdt', 0.0))]
             )}