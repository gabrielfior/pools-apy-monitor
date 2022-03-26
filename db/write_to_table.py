from typing import List
import datetime
import sqlalchemy
import dataclasses
import datetime
import pandas as pd
import os
import uuid

from aux_classes import PoolBalanceHolder

@dataclasses.dataclass
class APYWrapper:
    platform: str
    chain_name: str
    pool_address: str
    datetime_crawl: datetime.datetime
    auto_compound: bool
    apr: float
    lp_token_value: float
    tvl: float
    crawl_source: str


class DBWriter:

    def __init__(self, DATABASE_URL = None) -> None:
        if DATABASE_URL is None:
            DATABASE_URL = os.environ['DATABASE_URL_DIGITAL_OCEAN'].replace('postgres', 'postgresql')
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        self.TABLENAME = 'apys'
        self.TOKENSETS_TABLENAME = 'set_tracker'
        self.PORTFOLIO_TABLENAME = 'portfolio_gf'

    def write_apy(self, apy_value: APYWrapper):
        df = pd.DataFrame(dataclasses.asdict(apy_value), index=[0])
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')

    def write_all_apys(self, apy_values: List[APYWrapper]):
        df = pd.DataFrame([dataclasses.asdict(apy_value) for apy_value in apy_values])
        # cleanup
        df['apr'] = pd.to_numeric(df['apr'], errors='coerce')
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')

    def write_tokenset_value(self, dict_item):
        df = pd.DataFrame(dict_item, index=[0])
        df.to_sql(self.TOKENSETS_TABLENAME, self.engine, if_exists='append', index=False)
    
    def write_portfolio_values(self, identifier: str, apy_values: List[PoolBalanceHolder]):
        df = pd.DataFrame([dataclasses.asdict(apy_value) for apy_value in apy_values])
        df['datetime_crawl'] = datetime.datetime.now()
        df['crawl_id'] = str(uuid.uuid4())
        df['identifier'] = identifier
        # cleanup
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')

