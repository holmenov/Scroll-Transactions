from modules.account import Account
from utils.utils import send_logs


class BalanceChecker(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None, chain: str = 'scroll') -> None:
        super().__init__(account_id, private_key, proxy, chain)
    
    async def check_balance(self):
        try:
            balance, _ = await self.get_balance()
            
            send_logs(f'Current balance: {round(balance, 6)} $ETH.', self.account_id, self.address)
            
            return balance
        
        except Exception as error:
            send_logs(f'Error when balance checking: {error}', self.account_id, self.address, status='error')
            return False