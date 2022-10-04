from datetime import datetime

from db.write_to_table import APYWrapper, DBWriter
from scripts.beefy_fetcher import BeefyFetcher


def test_beefy_fetcher():
    database_url='postgresql://defai:rockettothemoon@159.223.12.238:5432/crawled_data'
    db = DBWriter(DATABASE_URL=database_url)
    apy_wrappers = []
    apys, lp_json, pool_addresses_and_chain = BeefyFetcher().fetch_daily_stats()
    for k, apy_value in apys.items():
        if 'totalApy' in apy_value and apy_value['totalApy'] is not None:
            apy = apy_value['totalApy']
        elif 'vaultApr' in apy_value and apy_value['vaultApr'] is not None:
            apy = apy_value['vaultApr']
        elif 'tradingApr' in apy_value and apy_value['tradingApr'] is not None:
            apy = apy_value['tradingApr']
        else:
            continue

        if apy is None:
            print ('found APY for {} none, continuing'.format(k))
            continue

        lp_value = lp_json[k] if k in lp_json else None
        chain, address = pool_addresses_and_chain.get(k, (None, None))

        apy_wrapper = APYWrapper(k,
                                 chain,
                                 address,
                                 datetime.now(),
                                 True,
                                 apy * 100,
                                 lp_value,
                                 tvl=None,
                                 crawl_source='beefy-test')
        apy_wrappers.append(apy_wrapper)

    db.write_all_apys(apy_wrappers)
    print ('test')