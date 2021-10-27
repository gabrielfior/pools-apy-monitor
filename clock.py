from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run

import os
from db.Platforms import Pools

from db.write_to_table import APYWrapper, DBWriter
from scripts.get_curve_base_apy import CurveFetcher

DATABASE_URL = os.environ['DATABASE_URL']

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=90)
def timed_job_pancake_manual():
    apr = run('scripts/get_pancake_manual')
    db = DBWriter()
    apy = APYWrapper(Pools.PANCAKE_SWAP_MANUAL_CAKE.value.platform_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.chain_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.pool_address,
                     datetime.now(),
                     False,
                     apr)
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
                                 apy*100)
        db.write_apy(apy_wrapper)


sched.start()
