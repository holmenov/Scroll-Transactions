"""
----------------------------------------MAIN SETTINGS------------------------------------------

    MAX_GAS - 40 | Gwei Control. Maximum value of GWEI in Ethereum for software operation.

    RANDOM_WALLETS - True | Take the wallets in random order.

    REMOVE_WALLET - True | To delete wallets after work or not. (IF NOT - SET FALSE).

    USE_PROXY - True | Use proxy or not.

    START_PERIOD_FROM = [1, 600] | The time period in which the wallets will be run.
        For example, wallets will be launched with a timer from 1 to 600 seconds after software launch.
            The first value is from, the second is to.
    
    REPEATS_PER_WALLET = 5 | The number of repetitions of each module.
    
    SLEEP_AFTER_WORK = [10, 30] | Sleeps after each module. A random number between 10 and 30 is selected.
    
    SLIPPAGE = 5 | Slippage in % for swaps.
    
    LANDINGS_SLEEP = [90, 300] | Sleep spacing for landing protocols. That's how long it will hold the money and withdraw after that time has elapsed.
    
    CUSTOM_ROUTES_MODULES = [                           |   With custom routes modules you can make your own routes.
        ['scroll_bridge'],                              |   One line - one transaction.
        ['izumi_swap', 'swap_syncswap'],                |   You can specify any number of functions on each line.
        ['wrap_eth', 'layerbank_deposit', None],        |   The software will select a random function in the list.
        ['layerbank_deposit', 'wrap_eth', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
    ]
    
---------------------------------------FUNCTIONS NAME------------------------------------------

    scroll_bridge           |   Bridge via official Scroll bridge.
    swap_syncswap           |   Swap on SyncSwap.
    izumi_swap              |   Swap on IzumiSwap.
    layerbank_deposit       |   Supply (Redeem) LayerBank.
    wrap_eth                |   Wrap (Unwrap) $ETH.
    send_mail               |   Send mail via DMail.
    increase_allowance      |   Increase Allowance to random address.
    approve                 |   Approve to random address.
    transfer                |   Transfer to random address.
    mint_nfts2me            |   Mint NFT on NFTS2ME.

-----------------------------------------------------------------------------------------------
"""

class MainSettings:
    MAX_GAS = 50 # GWEI

    RANDOM_WALLETS = True # True or False

    REMOVE_WALLET = True # True or False

    USE_PROXY = True # True or False

    START_PERIOD = [1, 600] # SECONDS, FROM AND TO

    REPEATS_PER_WALLET = 5 # REPEATS

    SLEEP_AFTER_WORK = [10, 30] # SECONDS, FROM AND TO
    
    SLIPPAGE = 5 # %

    LANDINGS_SLEEP = [90, 300] # SECONDS
    
    CUSTOM_ROUTES_MODULES = [
        ['scroll_bridge'],
        ['izumi_swap', 'swap_syncswap'],
        ['wrap_eth', 'layerbank_deposit', None],
        ['layerbank_deposit', 'wrap_eth', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
        ['send_mail', 'increase_allowance', 'approve', 'transfer', 'mint_nfts2me', None],
    ]

"""
---------------------------------------MODULE SETTINGS-----------------------------------------

    Each module has its own individual settings. Each module is labeled with the class "Module_Name".
    
    AMOUNT = [0.00035, 0.00065] | Amount for transactions. The program will take a random number in the specified interval.
    
    DECIMAL = 5 | Decimal places for rounding for a random transaction amount.
    
    FROM_TOKEN = 'ETH' | Tokens for swaps.
    TO_TOKEN = 'USDC' | In this example, we swap $ETH to $USDC.
    
    SWAP_REVERSE = True | Doing a reverse swap for the same amount?
    
    WITHDRAW = True | To withdraw liquidity from landing protocols or not.
    
    TOKENS = ['USDT'] | Token for modules linked to the token. You need to select any one of them from the list.
    
    NFT_CONTRACTS = {                                           
        '0x74670A3998d9d6622E32D0847fF5977c37E0eC91': 0,        |   List of contracts for NFT mint at NFT2ME.
        '0x80b1BDDc9a479cFA6F59c6eDd29A9cacEdBE7F91': 0.00005,  |   Provide the NFT contract address and the value of the mint in ETH.
    }                                                           

-----------------------------------------------------------------------------------------------
"""

class ModulesSettings:

    class ScrollBridge:   
        AMOUNT = [0.00035, 0.00065] # ETH
        DECIMAL = 5

    class SyncSwap:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.00035, 0.00065] # Amount in "FROM_TOKEN"
        DECIMAL = 5

        SWAP_REVERSE = True # True or False
    
    class IzumiSwap:
        FROM_TOKEN = 'ETH'
        TO_TOKEN = 'USDC'
        
        AMOUNT = [0.00035, 0.00065] # Amount in "FROM_TOKEN"
        DECIMAL = 5

        SWAP_REVERSE = True # True or False

    class LayerBank:
        AMOUNT = [0.00035, 0.00065] # ETH
        DECIMAL = 5
        
        WITHDRAW = True # True or False

    class WrapETH:
        AMOUNT = [0.00035, 0.00065] # ETH
        DECIMAL = 5
        
        UNWRAP_ETH = True # True or False

    class Tokens:

        class IncreaseAllowance: # ETH not avaliable
            TOKENS = ['USDT', 'USDC', 'DAI', 'WETH', 'WBTC', 'UNI'] # Choose one token

            AMOUNT = [0.000025, 0.000045] # Amount in "TOKENS"
            DECIMAL = 7
        
        class Approve: # ETH not avaliable
            TOKENS = ['USDT', 'USDC', 'DAI', 'WETH', 'WBTC', 'UNI'] # Choose one token

            AMOUNT = [0.000025, 0.000045] # Amount in "TOKENS"
            DECIMAL = 7

        class Transfer:
            TOKENS = ['ETH']

            AMOUNT = [0.000025, 0.000045] # Amount in "TOKENS"
            DECIMAL = 7
    
    class NFTs2Me:
        NFT_CONTRACTS = {
            '0x74670A3998d9d6622E32D0847fF5977c37E0eC91': 0,
            '0x80b1BDDc9a479cFA6F59c6eDd29A9cacEdBE7F91': 0.00005,
            '0x16D5E9bf8A8cc9eCE5A22095ffd2563568133B9c': 0.00005,
            '0x29F5cacba44832F2D2BeEb7D90896595B0C4775c': 0.00005,
            '0x9F8881d0aedE314eEB1c64E59971c7D03a82CaD4': 0.00005,
            '0xd0882Eb278cb7aa38b87Df13023A508Ddf5559A9': 0.00005,
            '0x90bB1E4747154De645967f62A58084A7F336baE5': 0.00005,
            '0x4d9C1535b0369C3B46E179559532D87aed56a6d1': 0.00005,
            '0x59c1dd22fe8ffbc64fef00a26116b042a73261dd': 0.00005,
            '0x49eaac10495326f6b4b29b97de601f5f392cbbc4': 0.00005,
            '0x3b627d6e75a621b97936cf957b87abde3fe54367': 0.00005,
            '0x96c49703ad51539454dea037a52a2003cd054f2f': 0.00005,
            '0x49b997cb3c48c6fb5730bc36fb90203311d1c0d3': 0.00005,
            '0x7bb379b885abbfa5c3ccc171efd991a98b42cc4c': 0.00005
        }
