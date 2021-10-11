from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run

import os
from db.Platforms import Pools

from db.write_to_table import APYWrapper, DBWriter

DATABASE_URL = os.environ['DATABASE_URL']

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=30)
def timed_job():
    apr = run('scripts/get_pancake_manual')
    db = DBWriter()
    apy = APYWrapper(Pools.PANCAKE_SWAP_MANUAL_CAKE.value.platform_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.chain_name,
                     Pools.PANCAKE_SWAP_MANUAL_CAKE.value.pool_address,
                     datetime.now(),
                     False,
                     apr)
    db.write_apy(apy)


sched.start()
