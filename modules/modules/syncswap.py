from time import time
from eth_abi import abi

from modules.account import Account
from settings import MainSettings as SETTINGS
from utils.config import SYNCSWAP_CLASSIC_POOL_ABI, SYNCSWAP_CLASSIC_POOL_DATA_ABI, SYNCSWAP_CONTRACTS, SYNCSWAP_ROUTER_ABI, ZERO_ADDRESS, SCROLL_TOKENS
from utils.wrappers import check_gas
from utils.utils import async_sleep, send_logs

class SyncSwap(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.router_contract = self.get_contract(SYNCSWAP_CONTRACTS["router"], SYNCSWAP_ROUTER_ABI)
    
    async def get_pool(self, from_token_addr: str, to_token_addr: str):
        contract = self.get_contract(SYNCSWAP_CONTRACTS['classic_pool'], SYNCSWAP_CLASSIC_POOL_ABI)
        
        pool_address = await contract.functions.getPool(from_token_addr, to_token_addr).call()

        return pool_address
    
    async def get_min_amount_out(self, pool_address: str, token_address: str, amount: int):
        pool_contract = self.get_contract(pool_address, SYNCSWAP_CLASSIC_POOL_DATA_ABI)
        
        min_amount_out = await pool_contract.functions.getAmountOut(token_address, amount, self.address).call()
        
        return int(min_amount_out - (min_amount_out / 100 * SETTINGS.SLIPPAGE))
    
    @check_gas
    async def swap(
        self, from_token: str, to_token: str, min_amount: float, max_amount: float, decimal: int, swap_reverse: bool
    ):
        try:
            send_logs(f'{from_token} -> {to_token} | Swap on SyncSwap.', self.account_id, self.address)

            amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimal)

            from_token_addr = self.w3.to_checksum_address(SCROLL_TOKENS[from_token])
            to_token_addr = self.w3.to_checksum_address(SCROLL_TOKENS[to_token])

            pool_address = await self.get_pool(from_token_addr, to_token_addr)
            
            if pool_address == ZERO_ADDRESS:
                return send_logs(f'Swap path {from_token} to {to_token} not found!', self.account_id, self.address, status='error')
            
            if from_token != 'ETH':
                await self.approve(amount_wei, from_token_addr, self.router_contract)
            
            tx_data = await self.get_tx_data(value=amount_wei if from_token == 'ETH' else 0)
                
            min_amount_out = await self.get_min_amount_out(pool_address, from_token_addr, amount_wei)
            
            steps = [{
                'pool': pool_address,
                'data': abi.encode(['address', 'address', 'uint8'], [from_token_addr, self.address, 1]),
                'callback': ZERO_ADDRESS,
                'callbackData': '0x'
            }]
            
            paths = [{
                'steps': steps,
                'tokenIn': ZERO_ADDRESS if from_token == 'ETH' else from_token_addr,
                'amountIn': amount_wei
            }]
            
            deadline = int(time()) + 1800
            
            tx = await self.router_contract.functions.swap(paths, min_amount_out, deadline).build_transaction(tx_data)
            
            await self.execute_transaction(tx)

            if swap_reverse:
                await async_sleep(10, 30, logs=False)
                await self.swap(to_token, from_token, min_amount_out, min_amount_out, decimal, False)
            
            return True

        except Exception as error:
            send_logs(f'Error when using SyncSwap: {error}', self.account_id, self.address, status='error')
            return False