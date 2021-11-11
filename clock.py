from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run

from pycoingecko import CoinGeckoAPI

from db.Platforms import Pools

from db.write_to_table import APYWrapper, DBWriter
from scripts.beefy_fetcher import BeefyFetcher
from scripts.get_curve_base_apy import CurveFetcher
from scripts.yearn_fetcher import YearnFetcher

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=90)
def timed_job_beefy():
    apys, lp_json, pool_addresses = BeefyFetcher().fetch_daily_stats()

    db = DBWriter()

    for k, address in pool_addresses.items():

        if k not in apys or apys[k]['totalApy'] is None:
            continue

        apy = apys[k]['totalApy']
        lp_value = lp_json[k] if k in lp_json else None

        apy_wrapper = APYWrapper(k,
                                 None,
                                 address,
                                 datetime.now(),
                                 True,
                                 apy * 100,
                                 lp_value)
        db.write_apy(apy_wrapper)


@sched.scheduled_job('interval', minutes=90)
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
                                 lp_price)
        db.write_apy(apy_wrapper)


@sched.scheduled_job('interval', minutes=90)
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
                     price_json[cake_address]['usd'])
    db.write_apy(apy)


@sched.scheduled_job('interval', minutes=90)
def timed_job_curve_base_apy():
    apys = CurveFetcher().fetch_daily_stats_curve()

    # We only return stats for aave and atricrypto3 since they are the most profitable ones.
    # Note that rewardAPYs are not tracked since not delivered by Curve Stats API.
    db = DBWriter()

    for apy, pool_enum in zip([apys['aave'], apys['atricrypto3']], [Pools.CURVE_AAVE, Pools.CURVE_ATRICRYPTO3]):
        print('Processing {}'.format(pool_enum))
        apy_wrapper = APYWrapper(pool_enum.value.platform_name,
                                 pool_enum.value.chain_name,
                                 pool_enum.value.pool_address,
                                 datetime.now(),
                                 False,
                                 apy * 100,
                                 None)  # no LP token available under this endpoint, to be determined if available elsewhere
        db.write_apy(apy_wrapper)


sched.start()