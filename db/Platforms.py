from enum import Enum
import dataclasses

@dataclasses.dataclass
class PoolWrapper:
    platform_name: str
    pool_address: str
    chain_name: str

class Pools(Enum):
    # platform name, pool contract address
    PANCAKE_SWAP_MANUAL_CAKE = PoolWrapper('pancakeswap', '0x73feaa1eE314F8c655E354234017bE2193C9E24E', 'bsc')
    PANCAKE_SWAPAUTO_CAKE = PoolWrapper('pancakeswap', '0xa80240Eb5d7E05d3F250cF000eEc0891d00b51CC', 'bsc')

class Tokens(Enum):
    CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'

class Networks(Enum):
    BSC_MAIN: 'bsc-main'