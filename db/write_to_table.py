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

class DBWriter:

    def __init__(self) -> None:
        DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
        #DATABASE_URL = 'postgresql://qyhodlgosoxuwr:1e848439d1daa4c1f089c28de1118cd37ea4a3db03d9a3fe5f97bf94f750784a@ec2-176-34-116-203.eu-west-1.compute.amazonaws.com:5432/depbto19usunbp'
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        self.TABLENAME = 'apys'
    
    def write_apy(self, apy_value: APYWrapper):
        df = pd.DataFrame(apy_value, index=[0])
        df.to_sql(self.TABLENAME, self.engine, if_exists='append')

if __name__ == "__main__":
    a = APYWrapper(0.45, 'dummy', '0x73feaa1eE314F8c655E354234017bE2193C9E24E', datetime.datetime.now())
    b = DBWriter()
    b.write_apy(dataclasses.asdict(a))