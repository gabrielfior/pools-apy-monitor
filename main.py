from brownie import run, network

network.connect('bsc-main')
a = run('scripts/get_pancake_manual')
print ('a {}'.format(a))
if network.is_connected():
    network.disconnect()
