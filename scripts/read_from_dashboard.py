'''
# get conversion rates
https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_last_updated_at=true

# wallets
https://api.apeboard.finance/wallet/bsc/0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57
https://api.apeboard.finance/wallet/terra/terra1g3zhdkmdwdlmqqrlqjjprz2ndpdrnarx3w2jq7
https://api.apeboard.finance/wallet/matic/0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8

# defi pools
https://api.apeboard.finance/pancakebunnyBsc/0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57
# https://api.apeboard.finance/pancakeswapBsc/0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57
https://api.apeboard.finance/mirrorTerra/terra1g3zhdkmdwdlmqqrlqjjprz2ndpdrnarx3w2jq7
https://api.apeboard.finance/curvePolygon/0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8
https://api.apeboard.finance/polycatPolygon/0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8
https://api.apeboard.finance/polycatPolygon/0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8
https://api.apeboard.finance/curvePolygon/0x2A333B3f9833558d583A6BADaBeCd62cE7A377b8
'''
import requests

url = 'https://api.apeboard.finance/pancakebunnyBsc/0xa1a65Db4D96eBD62e2Eb69B6a1983E5A9678fC57'
r = requests.get(url, headers={'access-control-request-headers':'ape-secret,passcode'})
print (r.status_code)
print (r.json())