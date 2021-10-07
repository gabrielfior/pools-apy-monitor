from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run, network

import os
import psycopg2
DATABASE_URL = os.environ['DATABASE_URL']

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    network.connect('bsc-main')
    apr = run('scripts/get_pancake_manual')
    print ('apr {}  ')
    network.disconnect()

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO pancake_manual_apy(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""


sched.start()