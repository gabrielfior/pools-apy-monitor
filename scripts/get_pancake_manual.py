manual_pancakeswap_pool = "0x73feaa1eE314F8c655E354234017bE2193C9E24E"
cake_token = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"
auto_cake_pool = "0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC"
bsc_api_token = 'RU7Y28HFEAFBU7EB9ZV1QHMSMDUZSHNY1Q'
'''
OK
    cake_per_block
    totalAllocPoint
    allocPoints
    numberOfBlocks
    blockReward
    annualBlockReward 
    lpSupply - ? 163298821012138285583292953

ERROR
    
    
    apr - ? 64.37
'''
from brownie import *

def main():
    print ('manual pancakeswap pool {}'.format(manual_pancakeswap_pool))

    print ('connecting to bsc main')
    if not network.is_connected():
        network.connect('bsc-main')

    try:
        contract = Contract(manual_pancakeswap_pool)
    except:
        print ('trying from explorer...')
        contract = Contract.from_explorer(manual_pancakeswap_pool)
    
    cakePerBlock = contract.cakePerBlock() 
    poolAllocPoint = contract.poolInfo("0")[1]
    totalAllocPoint = contract.totalAllocPoint()
    numberOfBlocks = 20 * 60 * 24 * 365
    blockReward = cakePerBlock*poolAllocPoint/totalAllocPoint
    annualBlockReward = blockReward*numberOfBlocks*1000000000000
    cakeContract = Contract(cake_token)

    lpSupply = cakeContract.balanceOf(manual_pancakeswap_pool)
    apr = annualBlockReward/(lpSupply*100000000*100) 
    print ('apr {} %'.format(round(apr, 2)))
    network.disconnect()
    return apr

# brownie run <script> --network bsc-main

# auto
#lpSupply = autoContract.balanceOf()
#cakeRewards = autoCakeContract.calculateHarvestCakeRewards()
# multiply by some constant
#constant = 4677397165079.107 #4.6*1e12
# The initial APY has been set based on the pool being compounded once per hour (8,670 times per year). 
# In actuality, the whole pool is likely to be compounded way more often than that, 