import requests
from collections import defaultdict
from db.Platforms import StatsUrls
import datetime
from db.write_to_table import APYWrapper


class MirrorFetcher:
    def __init__(self, apy_url=StatsUrls.MIRROR_APY.value):
        self.apy_url = apy_url

    def fetch_daily_stats(self):
        apys = requests.get(self.apy_url).json()

        daily_apys = defaultdict(list)
        assets = {}
        for i in apys:
            daily_apys[i['asset_id']].append({'apy_long': i['avg_long'], 'apy_short': i['avg_short'],
                                    'date': datetime.datetime.strptime(i['stat_date'], '%m-%d-%Y')})
            if i['asset_id'] not in assets:
                assets[i['asset_id']] = i['asset']

        return daily_apys, assets

    def organize_daily_stats(self, daily_apys, assets):
        apy_wrappers = []

        for k, v in daily_apys.items():
            pool_identifier = "{}-{}".format(assets[k]
                                             ['symbol'], assets[k]['token'])
            v.sort(key=lambda x: x['date'], reverse=True)
            v_max = v[0]

            apy_wrappers.append(APYWrapper(
                apr=v_max['apy_long']*100, platform='mirror',
                chain_name='terra',
                pool_address="{}-{}".format('long', pool_identifier), 
                datetime_crawl=v_max['date'],
                auto_compound=False, lp_token_value=None, tvl=None,crawl_source='mirrortracker'))

            apy_wrappers.append(APYWrapper(apr=v_max['apy_short']*100, 
            platform='mirror', chain_name='terra',
                        pool_address="{}-{}".format('short', pool_identifier), datetime_crawl=v_max['date'],
                        auto_compound=False, lp_token_value=None, tvl=None, crawl_source='mirrortracker'))

        return apy_wrappers