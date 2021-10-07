manual_pancakeswap_pool = "0x73feaa1eE314F8c655E354234017bE2193C9E24E"
cake_token = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"
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
from brownie import Contract

def main():

    contract = Contract(manual_pancakeswap_pool);
    cakePerBlock = contract.cakePerBlock() 
    poolAllocPoint = contract.poolInfo("0")[1]
    totalAllocPoint = contract.totalAllocPoint()
    numberOfBlocks = 20 * 60 * 24 * 365
    blockReward = cakePerBlock*poolAllocPoint/totalAllocPoint
    annualBlockReward = blockReward*numberOfBlocks*1000000000000
    cakeContract = contract.from_explorer(cake_token)

    lpSupply = cakeContract.balanceOf(manual_pancakeswap_pool)
    apr = annualBlockReward/(lpSupply*100000000*100) 
    print ('apr {} %'.format(round(apr, 2)))

# brownie run <script> --network --network bsc-main