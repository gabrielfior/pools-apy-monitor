# for accessing BSC chain
# brownie console --network bsc-main

# token price if needed ->https://api.pancakeswap.info/api/v2/tokens
pancake_pool_address = '0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC'
manual_cake_contract_address = '0x73feaa1eE314F8c655E354234017bE2193C9E24E'
gf_address = '0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57'

c = Contract.from_explorer(pancake_pool_address)

# next steps
# get ROY of pool
# integrate with chainlink
# integrate with Telegram

accounts.at(gf_address, force=True)

# number of cake staked by user == c.userInfo(gf_address)[2]/1e18

# total rewards = c.calculateTotalPendingCakeRewards()/1e18
# total shares = 71228030.34610058
# total cake staked in contract = c.balanceOf()/1e18

# total rewards = 39354859748370953301
# balanceOf = 84425444999571485040239151

# how to get balance in cake from contract?
######################


const stakingTokenPrice = stakingTokenAddress ? prices[stakingTokenAddress] : 0
const earningTokenPrice = earningTokenAddress ? prices[earningTokenAddress] : 0
totalStaked =  totalStaked/ stakingToken.decimals
tokenPerBlock = pool.tokenPerBlock

BLOCKS_PER_YEAR  = 10512000 ; # https://github.com/pancakeswap/pancake-frontend/blob/673d9f3b899a1123994a6ebf124d7c297e13a9a0/src/config/index.ts
  const totalRewardPricePerYear = new BigNumber(rewardTokenPrice).times(tokenPerBlock).times(BLOCKS_PER_YEAR)
  const totalStakingTokenInPool = new BigNumber(stakingTokenPrice).times(totalStaked)
  const apr = totalRewardPricePerYear.div(totalStakingTokenInPool).times(100)

