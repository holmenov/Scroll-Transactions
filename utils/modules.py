import random

from utils.utils import async_sleep
from settings import ModulesSettings as ms
from modules.modules.tokens import Tokens
from modules.modules.dmail import Dmail
from modules.modules.syncswap import SyncSwap
from modules.modules.wrap_eth import WrapETH
from modules.modules.nfts2me import NFT2Me
from modules.modules.izumi import Izumi
from modules.modules.scroll_bridge import ScrollBridge
from modules.modules.layerbank import LayerBank
from modules.modules.balance_checker import BalanceChecker


async def random_module(account_id, key, proxy):
    modules = [
        send_mail, swap_syncswap, wrap_eth,
        increase_allowance, approve, transfer
    ]
    choice = random.choice(modules)
    return await choice(account_id, key, proxy)

async def random_low_cost_module(account_id, key, proxy):
    modules = [
        send_mail, wrap_eth, increase_allowance,
        approve, transfer
    ]
    choice = random.choice(modules)
    return await choice(account_id, key, proxy)

async def low_cost_25_tx(account_id, key, proxy):
    modules = [
        mint_nfts2me, mint_nfts2me, mint_nfts2me, mint_nfts2me, mint_nfts2me,
        mint_nfts2me, mint_nfts2me, mint_nfts2me, mint_nfts2me, mint_nfts2me,
        send_mail, send_mail, send_mail, send_mail, send_mail,
        wrap_eth, swap_syncswap, approve, transfer, increase_allowance
    ]
    
    while modules:
        choice = random.choice(modules)
        modules.remove(choice)
        await choice(account_id, key, proxy)
        
        await async_sleep(5, 30, logs=False)
        
    return True

async def scroll_bridge(account_id, key, proxy):
    min_amount = ms.SyncSwap.AMOUNT[0]
    max_amount = ms.SyncSwap.AMOUNT[1]
    decimal = ms.SyncSwap.DECIMAL
    
    scrol_bridge = ScrollBridge(account_id, key, proxy)
    return await scrol_bridge.bridge(min_amount, max_amount, decimal)

async def swap_syncswap(account_id, key, proxy):
    from_token = ms.SyncSwap.FROM_TOKEN
    to_token = ms.SyncSwap.TO_TOKEN
    
    min_amount = ms.SyncSwap.AMOUNT[0]
    max_amount = ms.SyncSwap.AMOUNT[1]
    decimal = ms.SyncSwap.DECIMAL

    swap_reverse = ms.SyncSwap.SWAP_REVERSE
    
    syncswap = SyncSwap(account_id, key, proxy)
    return await syncswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, swap_reverse
    )

async def izumi_swap(account_id, key, proxy):
    from_token = ms.IzumiSwap.FROM_TOKEN
    to_token = ms.IzumiSwap.TO_TOKEN
    
    min_amount = ms.IzumiSwap.AMOUNT[0]
    max_amount = ms.IzumiSwap.AMOUNT[1]
    decimal = ms.IzumiSwap.DECIMAL

    swap_reverse = ms.IzumiSwap.SWAP_REVERSE

    izumiswap = Izumi(account_id, key, proxy)
    return await izumiswap.swap(
        from_token, to_token, min_amount, max_amount, decimal, swap_reverse
    )

async def layerbank_deposit(account_id, key, proxy):
    min_amount = ms.LayerBank.AMOUNT[0]
    max_amount = ms.LayerBank.AMOUNT[1]
    decimal = ms.LayerBank.DECIMAL
    
    withdraw = ms.LayerBank.WITHDRAW
    
    layerbank = LayerBank(account_id, key, proxy)
    return await layerbank.deposit(
        min_amount, max_amount, decimal, withdraw
    )

async def wrap_eth(account_id, key, proxy):
    min_amount = ms.WrapETH.AMOUNT[0]
    max_amount = ms.WrapETH.AMOUNT[1]
    decimal = ms.WrapETH.DECIMAL
    
    unwrap_eth = ms.WrapETH.UNWRAP_ETH
    
    wrap_eth = WrapETH(account_id, key, proxy)
    return await wrap_eth.wrap_eth(
        min_amount, max_amount, decimal, unwrap_eth
    )

async def send_mail(account_id, key, proxy):
    dmail = Dmail(account_id, key, proxy)
    return await dmail.send_mail()

async def increase_allowance(account_id, key, proxy):
    tokens = ms.Tokens.IncreaseAllowance.TOKENS
    
    min_amount = ms.Tokens.IncreaseAllowance.AMOUNT[0]
    max_amount = ms.Tokens.IncreaseAllowance.AMOUNT[1]
    decimals = ms.Tokens.IncreaseAllowance.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.increase_allowance(
        tokens, min_amount, max_amount, decimals
    )

async def approve(account_id, key, proxy):
    tokens = ms.Tokens.Approve.TOKENS
    
    min_amount = ms.Tokens.Approve.AMOUNT[0]
    max_amount = ms.Tokens.Approve.AMOUNT[1]
    decimals = ms.Tokens.Approve.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.approve_random_address(
        tokens, min_amount, max_amount, decimals
    )

async def transfer(account_id, key, proxy):
    tokens = ms.Tokens.Transfer.TOKENS
    
    min_amount = ms.Tokens.Transfer.AMOUNT[0]
    max_amount = ms.Tokens.Transfer.AMOUNT[1]
    decimals = ms.Tokens.Transfer.DECIMAL
    
    tokens_functions = Tokens(account_id, key, proxy)
    return await tokens_functions.transfer(
        tokens, min_amount, max_amount, decimals
    )

async def mint_nfts2me(account_id, key, proxy):
    nfts_contracts = ms.NFTs2Me.NFT_CONTRACTS

    tokens_functions = NFT2Me(account_id, key, proxy)
    return await tokens_functions.mint(nfts_contracts)


async def check_balance(account_id, key, proxy):
    balance_checker = BalanceChecker(account_id, key, proxy)
    return await balance_checker.check_balance()