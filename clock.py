from apscheduler.schedulers.blocking import BlockingScheduler

from brownie import run, network

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    network.connect('bsc-main')
    apr = run('scripts/get_pancake_manual')
    print ('apr {}  ')
    network.disconnect()


sched.start()