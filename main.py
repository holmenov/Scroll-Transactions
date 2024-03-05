import asyncio
from loguru import logger
import questionary
import sys

from utils.launch import run_check_balance, start_tasks
from utils.utils import get_wallets
from utils.modules import *


def start():
    start_menu = [
        questionary.Choice('🚀 Custom Module Routes', 'custom-routes'),
        questionary.Choice('✨ One Selected Module', 'one-module'),
        questionary.Choice('💼 Scroll Balance Checker', 'balance-checker'),
        questionary.Choice('❌ Exit', 'exit'),
    ]
    
    start_mode = questionary.select(
        'Select a mode to start the software:',
        choices=start_menu,
        qmark='📌 ',
        pointer='➡️ '
    ).ask()
    
    return start_mode


def one_selected_module():
    modules = [
        questionary.Choice('1) Random module', random_module),
        questionary.Choice('2) Random low-cost module', random_low_cost_module),
        questionary.Choice('3) Sending mail via DMail', send_mail),
        questionary.Choice('4) Swap on SyncSwap', swap_syncswap),
        questionary.Choice('5) Wrap ETH', wrap_eth),
        questionary.Choice('6) Increase allowance token', increase_allowance),
        questionary.Choice('7) Approve token', approve),
        questionary.Choice('8) Transfer token', transfer),
        questionary.Choice('9) Mint NFT on NFTs2ME', mint_nfts2me),
        questionary.Choice('10) Get cheap ~25 transactions', low_cost_25_tx),
    ]
    
    module = questionary.select(
        'Choose module to start:',
        choices=modules,
        qmark='📌 ',
        pointer='➡️ '
    ).ask()

    return module


def main():
    start_mode = start()
    
    if start_mode == 'exit': sys.exit()
    
    data = get_wallets()
    
    if start_mode == 'custom-routes':
        asyncio.run(start_tasks(data))

    elif start_mode == 'one-module':
        module = one_selected_module()
        asyncio.run(start_tasks(data, module))

    elif start_mode == 'balance-checker':
        asyncio.run(run_check_balance(data))
    

if __name__ == '__main__':
    logger.add('logs.log')
    main()