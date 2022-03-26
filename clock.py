from datetime import datetime
from typing import List
from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run
from apeboard_fetcher import ApeboardFetcher
from aux_classes import AccountHolder, PoolBalanceHolder

#from pycoingecko import CoinGeckoAPI

from db.Platforms import Pools

from db.write_to_table import APYWrapper, DBWriter
from scripts.beefy_fetcher import BeefyFetcher
from scripts.get_curve_base_apy import CurveFetcher
from scripts.mirror_fetcher import MirrorFetcher
from token_fetcher import TokenFetcher

sched = BlockingScheduler()

class FetchExecutor:
    def fetch_tokens(self, account: AccountHolder):
        tf = TokenFetcher({k:v for k,v in zip(
            ['solana','terra','bsc','matic','fantom','eth'],
            [account.account_solana, account.account_terra, account.account_bsc,
        account.account_polygon, account.account_polygon, account.account_polygon]) if v is not None})
        return tf.fetch_tokens()


    def fetch_pools(self, account: AccountHolder):
        af = ApeboardFetcher(account)
        return af.fetch_data()

@sched.scheduled_job('interval', minutes=45)
def timed_job_beefy():
    print ('processing job beefy')
    db = DBWriter()
    apy_wrappers = []
    apys, lp_json, pool_addresses_and_chain = BeefyFetcher().fetch_daily_stats()

    for k, apy_value in apys.items():
        if 'totalApy' in apy_value and apy_value['totalApy'] is not None:
            apy = apy_value['totalApy']
        elif 'vaultApr' in apy_value and apy_value['vaultApr'] is not None:
            apy = apy_value['vaultApr']
        elif 'tradingApr' in apy_value and apy_value['tradingApr'] is not None:
            apy = apy_value['tradingApr']
        else:
            continue

        lp_value = lp_json[k] if k in lp_json else None
        chain, address = pool_addresses_and_chain.get(k, (None, None))

        apy_wrapper = APYWrapper(k,
                                 chain,
                                 address,
                                 datetime.now(),
                                 True,
                                 apy * 100,
                                 lp_value,
                                 tvl=None,
                                 crawl_source='beefy')
        apy_wrappers.append(apy_wrapper)

    db.write_all_apys(apy_wrappers)
    print ('finished writing beefy pools to DB')

'''
@sched.scheduled_job('interval', minutes=60)
def timed_job_yearn():
    yf = YearnFetcher()
    apys = yf.fetch_daily_stats()

    db = DBWriter()

    for apy in apys:

        print ('processing {}'.format(apy['symbol']))
        apy_value = yf.fetch_apy_from_json(apy)
        # neglect pools with no funds locked
        if apy_value is None or apy['tvl'] is None:
            continue

        symbol = apy['symbol']
        pool_address = apy['address']

        lp_token_address = apy['token']['address']
        lp_price, chain_name = yf.fetch_token_price_using_all_networks(lp_token_address)

        apy_wrapper = APYWrapper(symbol,
                                 chain_name,
                                 pool_address,
                                 datetime.now(),
                                 None,
                                 apy_value * 100,
                                 lp_price,
                                 tvl=None,
                                 crawl_source='yearn')
        db.write_apy(apy_wrapper)
'''
'''
@sched.scheduled_job('interval', minutes=60)
def timed_job_pancake_manual():
    apr, cake_address = run('scripts/get_pancake_manual')

    cg = CoinGeckoAPI()
    price_json = cg.get_token_price(id='binance-smart-chain', vs_currencies='usd', contract_addresses=cake_address)

    db = DBWriter()
    apy = APYWrapper(Pools.PANCAKE_SWAP_MANUAL_CAKE.value.platform_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.chain_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.pool_address,
                     datetime.now(),
                     False,
                     apr,
                     price_json[cake_address]['usd'],
                                 tvl=None,
                                 crawl_source='pancake')
    db.write_apy(apy)
'''

@sched.scheduled_job('interval', minutes=45)
def timed_job_curve_base_apy():
    print ('processing job curve')
    apys = CurveFetcher().fetch_daily_stats_curve()

    # We only return stats for aave and atricrypto3 since they are the most profitable ones.
    # Note that rewardAPYs are not tracked since not delivered by Curve Stats API.
    db = DBWriter()

    for apy, pool_enum in zip([apys['aave'], apys['atricrypto3'], apys['eurtusd']], [Pools.CURVE_AAVE, Pools.CURVE_ATRICRYPTO3]):
        print('Processing {}'.format(pool_enum))
        apy_wrapper = APYWrapper(pool_enum.value.platform_name,
                                 pool_enum.value.chain_name,
                                 pool_enum.value.pool_address,
                                 datetime.now(),
                                 False,
                                 apy * 100,
                                 None,
                                 tvl=None,
                                 crawl_source='curve')  # no LP token available under this endpoint, to be determined if available elsewhere
        db.write_apy(apy_wrapper)

@sched.scheduled_job('interval', minutes=45)
def timed_job_token_sets():
    print ('processing job token sets')
    db = DBWriter()
    tokensets_dict = run('scripts/token_sets_fetcher')

    db.write_tokenset_value(tokensets_dict)

    print ('finished writing token sets to DB')


@sched.scheduled_job('interval', days=1)
def timed_job_mirror():
    print ('processing job mirror')
    db = DBWriter()
    mirror_fetcher = MirrorFetcher()
    
    daily_apys, assets = mirror_fetcher.fetch_daily_stats()
    apy_wrappers = mirror_fetcher.organize_daily_stats(daily_apys, assets)
    db.write_all_apys(apy_wrappers)
    print ('finished writing mirror pools to DB')

'''
@sched.scheduled_job('interval', minutes=45)
def timed_job_multifarm():
    print ('processing job multifarm')
    db = DBWriter()
    farm_info = MultifarmFetcher().fetch_daily_stats()
    apy_wrapper = APYWrapper('Anchor',
                          farm_info['blockchain'],
                          None,
                          datetime.now(),
                          False,
                          farm_info['aprYearly'],
                          None,
                          farm_info['tvlStaked'],
                          'multifarm')

    db.write_apy(apy_wrapper)
    print ('finished writing multifarm pools to DB')
'''

@sched.scheduled_job('interval', hours=6)
def timed_job_gf():
    print ('processing portfolio job gf')
    fe = FetchExecutor()
    db = DBWriter()
    
    account_polygon = '0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8'
    account_bsc = '0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57'
    account_solana = 'E9rgWo1Pb2g2PtcAcGTAWJgpBGV7cMATZuZf1DTnypWF'
    account_terra = 'terra1g3zhdkmdwdlmqqrlqjjprz2ndpdrnarx3w2jq7'
    account_near = '380560062d8eb0805755a8abf1e9a64b8d2bdd64466300e7287832ac797ca326'
    account_avax = '0x42DEF9Fd76CCa3636C8C5c3812458e5A4FBD9464'

    account_gf = AccountHolder(account_polygon, account_bsc, account_terra, account_solana)

    pool_list: List[PoolBalanceHolder] = fe.fetch_pools(account_gf)
    token_list: List[PoolBalanceHolder] = fe.fetch_tokens(account_gf)
    
    db.write_portfolio_values('gf', pool_list + token_list)
    print ('finished writing portfolio gf')

@sched.scheduled_job('interval', hours=6)
def timed_job_red():
    print ('processing portfolio job red')
    fe = FetchExecutor()
    db = DBWriter()
    
    account_red = AccountHolder('0x0631F77f628216F6f33E2EA13ADaA2feAca1807f', None, None, None)

    pool_list: List[PoolBalanceHolder] = fe.fetch_pools(account_red)
    token_list: List[PoolBalanceHolder] = fe.fetch_tokens(account_red)
    
    db.write_portfolio_values('red', pool_list + token_list)
    print ('finished writing portfolio red')

sched.start()