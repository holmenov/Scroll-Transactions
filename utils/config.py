import json


with open('accounts.txt', 'r') as file:
    ACCOUNTS = [row.strip() for row in file]
    
with open('proxy.txt', 'r') as file:
    PROXIES = [row.strip() for row in file]

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/erc20_abi.json', 'r') as file:
    ERC20_ABI = json.load(file)

with open('data/dmail/abi.json', 'r') as file:
    DMAIL_ABI = json.load(file)

with open('data/syncswap/router.json', 'r') as file:
    SYNCSWAP_ROUTER_ABI = json.load(file)

with open('data/syncswap/classic_pool.json', 'r') as file:
    SYNCSWAP_CLASSIC_POOL_ABI = json.load(file)

with open('data/syncswap/classic_pool_data.json', 'r') as file:
    SYNCSWAP_CLASSIC_POOL_DATA_ABI = json.load(file)

with open('data/weth/abi.json') as file:
    WETH_ABI = json.load(file)

with open('data/izumi/liquidity_manager_abi.json') as file:
    IZUMI_LIQUDITY_ABI = json.load(file)

with open('data/izumi/quoter_abi.json') as file:
    IZUMI_QUOTER_ABI = json.load(file)

with open('data/izumi/router_abi.json') as file:
    IZUMI_ROUTER_ABI = json.load(file)

with open('data/scroll_bridge/scroll_messenger.json') as file:
    SCROLL_MESSENGER_ABI = json.load(file)

with open('data/layerbank/abi.json') as file:
    LAYERBANK_ABI = json.load(file)

with open('data/nfts2me/abi.json') as file:
    NFTS2ME_ABI = json.load(file)


MAX_APPROVE = 2**256 - 1

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'


DMAIL_CONTRACT = {
    'dmail'                 : '0x47fbe95e981C0Df9737B6971B451fB15fdC989d9',
}

IZUMI_CONTRACTS = {
    'router'                : '0x2db0AFD0045F3518c77eC6591a542e326Befd3D7',
    'quoter'                : '0x3EF68D3f7664b2805D4E88381b64868a56f88bC4',
}

SCROLL_TOKENS = {
    'ETH'                   : '0x5300000000000000000000000000000000000004',
    'USDT'                  : '0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df',
    'USDC'                  : '0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4',
    'DAI'                   : '0xcA77eB3fEFe3725Dc33bccB54eDEFc3D9f764f97',
    'WETH'                  : '0x5300000000000000000000000000000000000004',
    'WBTC'                  : '0x3C1BCa5a656e69edCD0D4E36BEbb3FcDAcA60Cf1',
    'UNI'                   : '0x434cdA25E8a2CA5D9c1C449a8Cb6bCbF719233E8',
}

SYNCSWAP_CONTRACTS = {
    'router'                : '0x80e38291e06339d10aab483c65695d004dbd5c69',
    'classic_pool'          : '0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d',
}

IZUMI_CONTRACTS = {
    "quoter"                : '0x3EF68D3f7664b2805D4E88381b64868a56f88bC4',
    "router"                : '0x2db0AFD0045F3518c77eC6591a542e326Befd3D7',
    "liquidity_manager"     : '0x1502d025BfA624469892289D45C0352997251728',
}

SCROLL_CONTRACTS = {
    'bridge_messenger'      : '0x6774bcbd5cecef1336b5300fb5186a12ddd8b367',
}

LAYERBANK_CONTRACT = {
    'layerbank_core'        : '0xEC53c830f4444a8A56455c6836b5D2aA794289Aa',
    'layerbank_eth'         : '0x274C3795dadfEbf562932992bF241ae087e0a98C',
}