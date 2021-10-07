from brownie import run, network

network.connect('bsc-main')
a = run('scripts/get_pancake_manual')
print ('a {}'.format(a))
network.disconnect()
