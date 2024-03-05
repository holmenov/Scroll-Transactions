from time import time

from hexbytes import HexBytes
from modules.account import Account
from utils.wrappers import check_gas
from utils.config import IZUMI_CONTRACTS, IZUMI_LIQUDITY_ABI, IZUMI_QUOTER_ABI, IZUMI_ROUTER_ABI, SCROLL_TOKENS, ZERO_ADDRESS
from utils.utils import send_logs, async_sleep
from settings import MainSettings as SETTINGS

class Izumi(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
        
        self.router_contract = self.get_contract(IZUMI_CONTRACTS['router'], IZUMI_ROUTER_ABI)
        self.quoter_contract = self.get_contract(IZUMI_CONTRACTS['quoter'], IZUMI_QUOTER_ABI)
    
    async def get_min_amount_out(self, path: bytes, amount_wei: int):
        min_amount_out, _ = await self.quoter_contract.functions.swapAmount(amount_wei, path).call()

        return int(min_amount_out - (min_amount_out / 100 * SETTINGS.SLIPPAGE))
    
    def get_path(from_token_addr: str, to_token_addr: str):
        from_token_bytes = HexBytes(from_token_addr).rjust(20, b'\0')
        to_token_bytes = HexBytes(to_token_addr).rjust(20, b'\0')
        fee_bytes = (400).to_bytes(3, 'big')

        return from_token_bytes + fee_bytes + to_token_bytes
    
    @check_gas
    async def swap(
        self, from_token: str, to_token: str, min_amount: float, max_amount: float, decimals: int, swap_reverse: bool
    ):
        try:
            send_logs(f'{from_token} -> {to_token} | Swap on Izumi.', self.account_id, self.address)
        
            amount_wei, _ = await self.get_random_amount(from_token, min_amount, max_amount, decimals)
            
            from_token_address, to_token_address = SCROLL_TOKENS[from_token], SCROLL_TOKENS[to_token]
            
            if from_token != 'ETH':
                await self.approve(amount_wei, from_token_address, IZUMI_CONTRACTS['router'])
            
            tx_data = await self.get_tx_data(value=amount_wei if from_token == 'ETH' else 0)
            deadline = int(time()) + 1800
            path = self.get_path(from_token_address, to_token_address)
            min_amount_out = await self.get_min_amount_out(path, amount_wei)

            tx_params = self.router_contract.encodeABI(
                fn_name='swapAmount',
                args=[(
                    path,
                    self.address if to_token != 'ETH' else ZERO_ADDRESS,
                    amount_wei,
                    min_amount_out,
                    deadline
                )]
            )
            
            full_data = [tx_params]
            
            if from_token == 'ETH' or to_token == 'ETH':
                tx_additional_data = self.router_contract.encodeABI(
                    fn_name='unwrapWETH9' if from_token != 'ETH' else 'refundETH',
                    args=[
                        min_amount_out,
                        self.address
                    ] if from_token != 'ETH' else None
                )
                full_data.append(tx_additional_data)
            
            tx = await self.router_contract.functions.multicall(full_data).build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            if swap_reverse:
                await async_sleep(10, 30, logs=False)
                await self.swap(to_token, from_token, min_amount_out, min_amount_out, 5, False)

            return True

        except Exception as error:
            send_logs(f'Error when using Izumi: {error}', self.account_id, self.address, status='error')
            return False