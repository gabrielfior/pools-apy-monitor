from dataclasses import dataclass

@dataclass
class PoolBalanceHolder:
    symbol: str
    address: str
    balance: float
    price: float
    value_usd: float

@dataclass
class AccountHolder:
    account_polygon: str
    account_bsc: str
    account_terra: str
    account_solana: str