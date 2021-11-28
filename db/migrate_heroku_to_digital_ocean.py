import datetime
import sqlalchemy
import pandas as pd

DATABASE_URL = 'postgres://seusijfgypxjpl:3c8f70fd7ba93a19a054a29e26ba063eaccb9b14893fa88aab065253d8fc8de0@ec2-54-155-254-112.eu-west-1.compute.amazonaws.com:5432/defgufibr3ks7r'
DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')
# moved to digital ocean
DATABASE_URL_DIGITAL_OCEAN = 'postgres://defai:rockettothemoon@159.223.12.238:5432/crawled_data'
DATABASE_URL_DIGITAL_OCEAN = DATABASE_URL_DIGITAL_OCEAN.replace(
    'postgres', 'postgresql')

engine = sqlalchemy.create_engine(DATABASE_URL)
engine_do = sqlalchemy.create_engine(DATABASE_URL_DIGITAL_OCEAN)

df_heroku = pd.read_sql_table('apys', engine)
df_do = pd.read_sql_table('apys', engine_do)

original_num_rows = len(df_do)
rows_to_migrate = len(df_heroku)
print('original size df_digital_ocean {}'.format(df_do.shape))

if 'tvl' not in df_heroku:
    df_heroku['tvl'] = [None for i in range(len(df_heroku))]

if 'crawl_source' not in df_heroku:
    df_heroku['crawl_source'] = [None for i in range(len(df_heroku))]

print('writing {} rows from Heroku to Digital Ocean'.format(df_heroku.shape))

with engine_do.begin() as conn_do:
    df_heroku.to_sql('apys', con=conn_do, index=False, if_exists='append')

    df_do = pd.read_sql_table('apys', conn_do)
    rows_actually_migrated = len(df_do) - original_num_rows
    migration_rows_success = rows_actually_migrated == rows_to_migrate
    print('diff rows matches - rows to migrate {}, rows_actually_migrated {} matches {}'.format(
        rows_to_migrate, rows_actually_migrated, migration_rows_success))

    if migration_rows_success:
        engine.execute('delete from apys')
    else:
        raise Exception('rows migrated do not match, abort.')

    