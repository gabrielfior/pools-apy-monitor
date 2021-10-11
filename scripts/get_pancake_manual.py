from db.Platforms import Pools, Tokens, Networks
from brownie import *

def get_contract_by_address(address):
    try:
        print ('trying by accessing network')
        contract = Contract(address)
    except:
        print ('trying from explorer...')
        contract = Contract.from_explorer(address)
    return contract

def connect_safe():
    if not network.is_connected():
        network.connect(Networks.BSC_MAIN.value)

def disconnect_safe():
    if network.is_connected():
        network.disconnect()

def main():
    manual_pancakeswap_pool = Pools.PANCAKE_SWAP_MANUAL_CAKE.value.pool_address
    cake_token = Tokens.CAKE.value

    connect_safe()

    contract = get_contract_by_address(manual_pancakeswap_pool)    
    cakePerBlock = contract.cakePerBlock() 
    poolAllocPoint = contract.poolInfo("0")[1]
    totalAllocPoint = contract.totalAllocPoint()
    numberOfBlocks = 20 * 60 * 24 * 365
    blockReward = cakePerBlock*poolAllocPoint/totalAllocPoint
    annualBlockReward = blockReward*numberOfBlocks*1000000000000

    cakeContract = get_contract_by_address(cake_token)

    lpSupply = cakeContract.balanceOf(manual_pancakeswap_pool)
    apr = annualBlockReward/(lpSupply*100000000*100)

    disconnect_safe()

    return apr

# brownie run <script> --network bsc-main

# auto
#lpSupply = autoContract.balanceOf()
#cakeRewards = autoCakeContract.calculateHarvestCakeRewards()
# multiply by some constant
#constant = 4677397165079.107 #4.6*1e12
# The initial APY has been set based on the pool being compounded once per hour (8,670 times per year). 
# In actuality, the whole pool is likely to be compounded way more often than that, 