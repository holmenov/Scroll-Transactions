from modules.account import Account
from utils.config import WETH_ABI, SCROLL_TOKENS
from utils.wrappers import check_gas
from utils.utils import send_logs, async_sleep


class WrapETH(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.weth_contract = self.get_contract(SCROLL_TOKENS['WETH'], WETH_ABI)
    
    @check_gas
    async def wrap_eth(self, min_amount: float, max_amount: float, decimal: int, unwrap_eth: bool):
        try:
            send_logs(f'Wrap $ETH.', self.account_id, self.address)

            amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal,)
            
            tx_data = await self.get_tx_data(value=amount_wei)
            
            tx = await self.weth_contract.functions.deposit().build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            if unwrap_eth:
                await async_sleep(10, 30, logs=False)
                await self.unwrap_eth()
            
            return True

        except Exception as error:
            send_logs(f'Error when using wrap $ETH: {error}', self.account_id, self.address, status='error')
            return False

    @check_gas
    async def unwrap_eth(self):
        try:
            send_logs(f'Unwrap $ETH.', self.account_id, self.address)

            _, balance_wei = await self.get_balance(SCROLL_TOKENS['WETH'])

            tx_data = await self.get_tx_data()

            tx = await self.weth_contract.functions.withdraw(balance_wei).build_transaction(tx_data)

            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when using unwrap $ETH: {error}', self.account_id, self.address, status='error')
            return False