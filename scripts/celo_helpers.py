from pycoingecko import CoinGeckoAPI
from brownie import Contract

celoTokens = [
    {"id": "ubeswap", "symbol": "UBE",
        "contract": "0x00be915b9dcf56a3cbe739d9b9c202ca692409ec"},
    {"id": "celo-dollar", "symbol": "CUSD",
        "contract": "0x64dEFa3544c695db8c535D289d843a189aa26b98"},
    {"id": "moola-market", "symbol": "MOO",
        "contract": "0x17700282592D6917F6A73D0bF8AcCf4D578c131e"},
    {"id": "wrapped-celo", "symbol": "WCELO",
        "contract": "0x471ece3750da237f93b8e339c536989b8978a438"},
    {"id": "wrapped-bitcoin", "symbol": "WBTC",
        "contract": "0xD629eb00dEced2a080B7EC630eF6aC117e614f1b"},
    {"id": "usd-coin", "symbol": "USDC",
        "contract": "0x765DE816845861e75A25fCA122bb6898B8B1282a"},
    {"id": "weth", "symbol": "WETH",
        "contract": "0x2DEf4285787d58a2f811AF24755A8150622f4361"},
    {"id": "sushi", "symbol": "SUSHI",
        "contract": "0xD15EC721C2A896512Ad29C671997DD68f9593226"}
]


class CeloHelper:

    def __init__(self) -> None:
        self.cg = CoinGeckoAPI()

    def getCeloPrices(self):
        idPrices = self.lookUpPrices([x['id'] for x in celoTokens])
        prices = {}
        for bt in celoTokens:
            if (bt['id'] in idPrices):
                prices[bt['contract']] = idPrices[bt['id']]
        return prices

    def lookUpPrices(self, id_array):
        prices = {}
        price_json = self.cg.get_price(ids=id_array, vs_currencies='usd')

        for k, v in price_json:
            prices[k] = v['usd']

        return prices


class CeloReward:
    def __init__(self) -> None:
        pass

    def loadMultipleRewardsUbeSynthetixPools(self, App, tokens, prices, pools):
        totalStaked = 0, totalUserStaked = 0, individualAPRs = [], infos = [], totalApr = 0
        for p in pools:
            info_pool = self.loadMultipleRewardsUbePoolInfo(App, tokens, prices, p.abi, p.address, p.numRewards)
            infos.append(info_pool)

        for i in infos:
            p= printUbeSynthetixPool(App, i, "celo")
            if p['staked_tvl'] is not None:
                totalStaked += p.staked_tvl
            if p['userStaked'] is not None:
                totalUserStaked += p.userStaked
                individualAPRs.append(p.userStaked * p.apr / 100)


        if totalUserStaked > 0:
            totalApr=sum(individualAPRs) / totalUserStaked

        return {'staked_tvl': totalStaked, 'totalUserStaked': totalUserStaked, 'totalApr': totalApr}

    def loadMultipleRewardsUbePoolInfo(App, tokens, prices, stakingAbi, stakingAddress, rewardsNumber):
      STAKING_POOL = Contract(stakingAddress, stakingAbi, App.provider)
  
      stakeTokenAddress = STAKING_POOL.stakingToken();
      rewardsNum = rewardsNumber - 1  #you are receiving one address from another function
      internalRewardTokenAddress = STAKING_POOL.rewardsToken(); #celo token
  
      rewardTokenAddresses = []
      for i in range(rewardsNum):
        rewardTokenAddress = STAKING_POOL.externalRewardsTokens(i); #0 token is UBE, 1 token is MOO
        rewardTokenAddresses.append(rewardTokenAddress)
      
      rewardTokenAddresses.push(internalRewardTokenAddress)
  
      stakeToken = await getCeloToken(App, stakeTokenAddress, stakingAddress);
      stakeToken.staked = await STAKING_POOL.totalSupply() / 10 ** stakeToken.decimals;
  
      var newPriceAddresses = stakeToken.tokens.filter(x =>
        !getParameterCaseInsensitive(prices, x));
      var newPrices = await lookUpTokenPrices(newPriceAddresses);
      for (const key in newPrices) {
        if (newPrices[key]?.usd)
            prices[key] = newPrices[key];
      }
      var newTokenAddresses = stakeToken.tokens.filter(x =>
        !getParameterCaseInsensitive(tokens,x));
      for (const address of newTokenAddresses) {
          tokens[address] = await getCeloToken(App, address, stakingAddress);
      }
  
      for(let rewardTokenAddress of rewardTokenAddresses){
        if (!getParameterCaseInsensitive(tokens, rewardTokenAddress)) {
          tokens[rewardTokenAddress] = await getCeloToken(App, rewardTokenAddress, stakingAddress);
        }
      }
  
      let rewardTokens = [];
      for(let rewardTokenAddress of rewardTokenAddresses){
        const rewardToken = getParameterCaseInsensitive(tokens, rewardTokenAddress);
        rewardTokens.push(rewardToken);
      }
  
      let rewardTokenTickers = [];
      for(let rewardToken of rewardTokens){
        const rewardTokenTicker = rewardToken.symbol;
        rewardTokenTickers.push(rewardTokenTicker);
      }
  
      const poolPrices = getPoolPrices(tokens, prices, stakeToken, "celo");
  
      if (!poolPrices)
      {
        console.log(`Couldn't calculate prices for pool ${stakeTokenAddress}`);
        return null;
      }
  
      const stakeTokenTicker = poolPrices.stakeTokenTicker;
  
      const stakeTokenPrice =
          prices[stakeTokenAddress]?.usd ?? getParameterCaseInsensitive(prices, stakeTokenAddress)?.usd;
  
      let rewardTokenPrices = [];
      for(let rewardTokenAddress of rewardTokenAddresses){
        const rewardTokenPrice = getParameterCaseInsensitive(prices, rewardTokenAddress)?.usd;
        rewardTokenPrices.push(rewardTokenPrice);
      }
  
      let weeklyRewards = [];
      let usdCoinsPerWeek = [];
  
      let rewardRateA = 0;
      let weeklyRewardA = 0;
      let usdPerWeekA = 0;
  
      if(rewardTokens.length > 2){
        rewardRateA = await STAKING_POOL.rewardRate();
        weeklyRewardA = rewardRateA / 10 ** rewardTokens[2].decimals * 604800;
        usdPerWeekA = weeklyRewardA * rewardTokenPrices[2];
        weeklyRewards.push(weeklyRewardA);
        usdCoinsPerWeek.push(usdPerWeekA);
  
        try{
          const nextRewardAddressB = await STAKING_POOL.externalStakingRewards();
          const nextRewardContractB = new ethers.Contract(nextRewardAddressB, stakingAbi, App.provider);
          const rewardRateB = await nextRewardContractB.rewardRate();
          const weeklyRewardB = rewardRateB / 10 ** rewardTokens[1].decimals * 604800;
          const usdPerWeekB = weeklyRewardB * rewardTokenPrices[1];
          weeklyRewards.push(weeklyRewardB);
          usdCoinsPerWeek.push(usdPerWeekB);
    
          try{
            const nextRewardAddressC = await nextRewardContractB.externalStakingRewards();
            const nextRewardContractC = new ethers.Contract(nextRewardAddressC, stakingAbi, App.provider);
            const rewardRateC = await nextRewardContractC.rewardRate();
            const weeklyRewardC = rewardRateC / 10 ** rewardTokens[0].decimals * 604800;
            const usdPerWeekC = weeklyRewardC * rewardTokenPrices[0];
            weeklyRewards.push(weeklyRewardC);
            usdCoinsPerWeek.push(usdPerWeekC);
          }
          catch(ex){
            console.log("There is no other reward contract");
          }
          
        }catch(ex){
          console.log("There is no other reward contract");
        }
      }else{
        rewardRateA = await STAKING_POOL.rewardRate();
        weeklyRewardA = rewardRateA / 10 ** rewardTokens[1].decimals * 604800;
        usdPerWeekA = weeklyRewardA * rewardTokenPrices[1];
        weeklyRewards.push(weeklyRewardA);
        usdCoinsPerWeek.push(usdPerWeekA);
  
        try{
          const nextRewardAddressB = await STAKING_POOL.externalStakingRewards();
          const nextRewardContractB = new ethers.Contract(nextRewardAddressB, stakingAbi, App.provider);
          const rewardRateB = await nextRewardContractB.rewardRate();
          const weeklyRewardB = rewardRateB / 10 ** rewardTokens[0].decimals * 604800;
          const usdPerWeekB = weeklyRewardB * rewardTokenPrices[0];
          weeklyRewards.push(weeklyRewardB);
          usdCoinsPerWeek.push(usdPerWeekB);        
        }catch(ex){
          console.log("There is no other reward contract");
        }
      }
  
      let earnings = [];
      for(let i = 0; i < 2; i++){
        const earned = await STAKING_POOL.externalRewards(App.YOUR_ADDRESS, rewardTokenAddresses[i]) / 10 ** rewardTokens[i].decimals;
        earnings.push(earned);
      }
      if(rewardTokens.length > 2){
        const earned = await STAKING_POOL.earned(App.YOUR_ADDRESS) / 10 ** rewardTokens[2].decimals;
        earnings.push(earned);
        //usdCoinsPerWeek.swapItems(0, 2);
        rewardTokenTickers.swapItems(0, 2);
      }else{
        //usdCoinsPerWeek.swapItems(0, 1);
        rewardTokenTickers.swapItems(0, 1);
      }
  
      const staked_tvl = poolPrices.staked_tvl;
  
      const userStaked = await STAKING_POOL.balanceOf(App.YOUR_ADDRESS) / 10 ** stakeToken.decimals;
  
      const userUnstaked = stakeToken.unstaked;
  
      return  {
        stakingAddress,
        poolPrices,
        stakeTokenAddress,
        rewardTokenAddresses,
        stakeTokenTicker,
        rewardTokenTickers,
        stakeTokenPrice,
        rewardTokenPrices,
        weeklyRewards,
        usdCoinsPerWeek,
        staked_tvl,
        userStaked,
        userUnstaked,
        earnings
      }
  }
