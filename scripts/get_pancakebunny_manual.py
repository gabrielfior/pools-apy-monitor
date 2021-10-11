manual_pancakebunny_pool = "0xEDfcB78e73f7bA6aD2D829bf5D462a0924da28eD"
cake_token = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"
bsc_api_token = 'RU7Y28HFEAFBU7EB9ZV1QHMSMDUZSHNY1Q'

from brownie import *

def get_contract_by_address(address):
    try:
        print ('trying by accessing network')
        contract = Contract(address)
    except:
        print ('trying from explorer...')
        contract = Contract.from_explorer(address)
    return contract

def main():
    print ('manual pancakeswap pool {}'.format(manual_pancakebunny_pool))

    print ('connecting to bsc main')
    if not network.is_connected():
        network.connect('bsc-main')

    contract = get_contract_by_address(manual_pancakebunny_pool)    
    cakePerBlock = contract.cakePerBlock() 
    poolAllocPoint = contract.poolInfo("0")[1]
    totalAllocPoint = contract.totalAllocPoint()
    numberOfBlocks = 20 * 60 * 24 * 365
    blockReward = cakePerBlock*poolAllocPoint/totalAllocPoint
    annualBlockReward = blockReward*numberOfBlocks*1000000000000

    cakeContract = get_contract_by_address(cake_token)

    lpSupply = cakeContract.balanceOf(manual_pancakebunny_pool)
    apr = annualBlockReward/(lpSupply*100000000*100) 
    print ('apr {} %'.format(round(apr, 2)))

    if network.is_connected():
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