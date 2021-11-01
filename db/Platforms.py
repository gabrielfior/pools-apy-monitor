from enum import Enum
import dataclasses


@dataclasses.dataclass
class PoolWrapper:
    platform_name: str
    pool_address: str
    chain_name: str


class Networks(Enum):
    BSC_MAIN = 'bsc-main'
    POLYGON_MAIN = 'polygon-main'
    ETHEREUM_MAINNET = 'mainnet'


class Pools(Enum):
    # platform name, pool contract address
    PANCAKE_SWAP_MANUAL_CAKE = PoolWrapper('pancakeswap', '0x73feaa1eE314F8c655E354234017bE2193C9E24E',
                                           Networks.BSC_MAIN.value)
    PANCAKE_SWAPAUTO_CAKE = PoolWrapper('pancakeswap', '0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC',
                                        Networks.BSC_MAIN.value)
    CURVE_ATRICRYPTO3 = PoolWrapper('curve', '0x92215849c439E1f8612b6646060B4E3E5ef822cC', Networks.POLYGON_MAIN.value)
    CURVE_AAVE = PoolWrapper('curve', '0x445FE580eF8d70FF569aB36e80c647af338db351', Networks.POLYGON_MAIN.value)


class Tokens(Enum):
    CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'


class StatsUrls(Enum):
    POLYGON_CURVE = 'https://stats.curve.fi/raw-stats-polygon/apys.json'
    BEEFY_FINANCE_APY = 'https://api.beefy.finance/apy/breakdown'
    BEEFY_FINANCE_LP = 'https://api.beefy.finance/lps'
    BEEFY_FINANCE_POOL_ADDRESSES = 'https://raw.githubusercontent.com/beefyfinance/beefy-app/prod/src/features/configure/vault/polygon_pools.js'
    YEARN_FINANCE = 'https://vaults.finance/all'
