from typing import List

import sqlalchemy
import dataclasses
import datetime
import pandas as pd
import os


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
            DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        self.TABLENAME = 'apys'

    def write_apy(self, apy_value: APYWrapper):
        df = pd.DataFrame(dataclasses.asdict(apy_value), index=[0])
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')

    def write_all_apys(self, apy_values: List[APYWrapper]):
        df = pd.DataFrame([dataclasses.asdict(apy_value) for apy_value in apy_values])
        # cleanup
        df['apr'] = pd.to_numeric(df['apr'], errors='coerce')
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')
