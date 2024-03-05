from modules.account import Account
from utils.utils import send_logs
from utils.wrappers import check_gas
from utils.config import SCROLL_MESSENGER_ABI, SCROLL_CONTRACTS


class ScrollBridge(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None, chain: str = 'ethereum') -> None:
        super().__init__(account_id, private_key, proxy, chain=chain)
        
        self.messenger_contract = self.get_contract(SCROLL_CONTRACTS['bridge_messenger'], SCROLL_MESSENGER_ABI)
    
    @check_gas
    async def bridge(self, min_amount: float, max_amount: float, decimal: int):
        send_logs('Bridge to Scroll.', self.account_id, self.address)
        
        amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal)
        
        _, balance_wei = await self.get_balance()
        
        if balance_wei > amount_wei:
            tx_data = await self.get_tx_data(value=amount_wei)
            
            data = [
                self.w3.to_checksum_address(self.address),
                int(amount_wei),
                bytes(0),
                int(168000)
            ]
            
            tx = await self.messenger_contract.functions.sendMessage(*data).build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            return True
        
        else:
            send_logs('Insufficient balance for Scroll Bridge.', self.account_id, self.address, status='error')
            return False