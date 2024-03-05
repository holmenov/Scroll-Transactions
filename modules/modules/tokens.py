import random

from modules.account import Account
from utils.config import ERC20_ABI, SCROLL_TOKENS
from utils.utils import get_random_address, send_logs
from utils.wrappers import check_gas


class Tokens(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
    
    @check_gas
    async def increase_allowance(self, tokens: list, min_amount: float, max_amount: float, decimal: int):
        try:
            token = random.choice(tokens)
            
            send_logs(f'Increase allowance ${token} to random address.', self.account_id, self.address)
            
            amount_wei, _ = await self.get_random_amount(token, min_amount, max_amount, decimal)
            
            token_contract = self.get_contract(SCROLL_TOKENS[token], ERC20_ABI)
            
            random_address = get_random_address()

            tx_data = await self.get_tx_data()

            tx = await token_contract.functions.increaseAllowance(random_address, amount_wei).build_transaction(tx_data)

            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when using increase allowance: {error}', self.account_id, self.address, status='error')
            return False
    
    @check_gas
    async def approve_random_address(self, tokens: list, min_amount: float, max_amount: float, decimals: int):
        try:
            token = random.choice(tokens)
            
            send_logs(f'Approve ${token} to random address.', self.account_id, self.address)
            
            amount_wei, _ = await self.get_random_amount(token, min_amount, max_amount, decimals)
            
            random_address = get_random_address()
            
            await self.approve(amount_wei, SCROLL_TOKENS[token], random_address)
            
            return True

        except Exception as error:
            send_logs(f'Error when using random approve: {error}', self.account_id, self.address, status='error')
            return False

    @check_gas
    async def transfer(self, tokens: list, min_amount: float, max_amount: float, decimals: int):
        try:
            chosen_token = random.choice(tokens)
            
            send_logs(f'Transfer ${chosen_token} to random address.', self.account_id, self.address)
            
            amount_wei, _ = await self.get_random_amount(chosen_token, min_amount, max_amount, decimals)
            
            tx = await self.get_tx_data()

            random_address = get_random_address()
            
            if chosen_token == 'ETH':
                tx.update({'to': random_address, 'value': amount_wei})

            else:
                token_contract = self.get_contract(SCROLL_TOKENS[chosen_token], ERC20_ABI)
                tx = await token_contract.functions.transfer(random_address, amount_wei).build_transaction(tx)

            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when using random transfer: {error}', self.account_id, self.address, status='error')
            return False