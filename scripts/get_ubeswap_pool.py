from brownie import web3
from scripts.celo_helpers import CeloHelper
from ube_consts import UBE_MULTI_REWARDS_ABI, UBE_STAKING_ABI

celoNode = 'https://alfajores-forno.celo-testnet.org'
web3.connect(celoNode)

addresses = [
    "0x295D6f96081fEB1569d9Ce005F7f2710042ec6a1",  # UBE-CELO
    "0x76183478939C414801C863222854efcc33791144",  # mcUSD-cBTC
    "0x5E37376AEcc2825dfdE04C3981968153c14B669c",  # cETH-mcUSD
    "0xC087aEcAC0a4991f9b0e931Ce2aC77a826DDdaf3",  # MOO-mCELO
    "0x66bD2eF224318cA5e3A93E165e77fAb6DD986E89",  # CELO-mcUSD
    "0xC88B8d622c0322fb59ae4473D7A1798DE60785dD",  # POOF-UBE
    "0x9dBfe0aBf21F506525b5bAD0cc467f2FAeBe40a1",  # UBE-cMCO2
    "0xd4C9675b0AE1397fC5b2D3356736A02d86347f2d",  # sCELO-CELO
    "0xD7D6b5213b9B9DFffbb7ef008b3cF3c677eb2468",  # rCELO-CELO
    "0x33F819986FE80A4f4A9032260A24770918511849",  # LAPIS-CELO
    "0xD409B7C4F67F5C845c53505b3d3B5aCD44e479AB",  # POOF-UBE
    "0x572564B0efEC39Dd325138187F5DD4e75B17251E",  # UBE-mcEURLPPool
    "0x342B20b1290a442eFDBEbFD3FE781FE79b3124b7",  # UBE-mcUSDLPPool
    "0x66bD2eF224318cA5e3A93E165e77fAb6DD986E89",  # mcUSD-CELOLPPool
    "0x08252f2E68826950d31D268DfAE5E691EE8a2426",  # mcEUR-CELOLPPool
    "0xaf13437122cd537C5D8942f17787cbDBd787fE94"  # mcEUR-mcUSDLPPool
]

multiRewardsPools = [
    # UBE-CELO
    {
        'address': '0x9D87c01672A7D02b2Dc0D0eB7A145C7e13793c3B',
        'underlyingPool': '0x295D6f96081fEB1569d9Ce005F7f2710042ec6a1',
        'basePool': '0x295D6f96081fEB1569d9Ce005F7f2710042ec6a1',
        'numRewards': 2,
        'active': True,
    }]

multiRewardsPools = [{
    'address': mrp.address,
    'abi': UBE_MULTI_REWARDS_ABI,
    'numRewards': mrp.numRewards
} for mrp in multiRewardsPools]

celo_helper = CeloHelper()

tokens = {}
prices = celo_helper.getCeloPrices()


pools = [{
    'address': a,
    'abi': UBE_STAKING_ABI,
    'stakeTokenFunction': "stakingToken",
    'rewardTokenFunction': "rewardsToken"
} for a in addresses]

# multi rewards ube
mrp = loadMultipleRewardsUbeSynthetixPools(App, tokens, prices, MultiRewardsPools)
print('Total staked: {}'.format(mrp.staked_tvl))
if mrp.totalUserStaked > 0:
    print('You are staking a total of $${formatMoney()} at an APR of ${.}%'.format(
        mrp['totalUserStaked'], mrp['totalAPR'] * 100))


# multi rewards celo
p = loadMultipleCeloSynthetixPools(App, tokens, prices, pools)
# _print_bold(`Total staked: $${formatMoney(p.staked_tvl)}`);
print('Total staked: {}'.format(p.staked_tvl))
if (p['totalUserStaked'] > 0):
    print('You are staking a total of {} at an APR of {}'.format((p['totalUserStaked'], p['totalAPR'] * 100)))
