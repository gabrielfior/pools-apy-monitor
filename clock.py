from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run

import os
from db.Platforms import Pools

from db.write_to_table import APYWrapper, DBWriter
DATABASE_URL = os.environ['DATABASE_URL']

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    apr = run('scripts/get_pancake_manual')
    db = DBWriter()
    apy = APYWrapper(apr, Pools.PANCAKE_SWAP_MANUAL_CAKE.value.platform_name,
        Pools.PANCAKE_SWAP_MANUAL_CAKE.value.chain_name, datetime.now(), apr, False)
    db.write_apy(apy)

sched.start()