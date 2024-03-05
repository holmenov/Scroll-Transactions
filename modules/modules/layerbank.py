from modules.account import Account
from utils.config import LAYERBANK_ABI, LAYERBANK_CONTRACT, ERC20_ABI
from utils.wrappers import check_gas
from utils.utils import send_logs, async_sleep
from settings import MainSettings as SETTINGS


class LayerBank(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.landing_contract = self.get_contract(LAYERBANK_CONTRACT['layerbank_core'], LAYERBANK_ABI)
        self.layerbank_eth_contract = self.get_contract(LAYERBANK_CONTRACT['layerbank_eth'], ERC20_ABI)
        
        self.layerbank_eth_addr = self.w3.to_checksum_address(LAYERBANK_CONTRACT['layerbank_eth'])
    
    @check_gas
    async def deposit(self, min_amount: float, max_amount: float, decimal: int, withdraw: bool):
        try:
            send_logs(f'Deposit to LayerBank.', self.account_id, self.address)

            amount_wei, _ = await self.get_random_amount('ETH', min_amount, max_amount, decimal)
            
            tx_data = await self.get_tx_data(value=amount_wei)
            
            tx = await self.landing_contract.functions.supply(self.layerbank_eth_addr, amount_wei).build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            if withdraw:
                await async_sleep(SETTINGS.LANDINGS_SLEEP[0], SETTINGS.LANDINGS_SLEEP[1], logs=False)
                await self.redeem_tokens()
            
            return True

        except Exception as error:
            send_logs(f'Error when deposit to LayerBank: {error}', self.account_id, self.address, status='error')
            return False
    
    @check_gas
    async def redeem_tokens(self):
        try:
            send_logs(f'Redeem tokens LayerBank.', self.account_id, self.address)
            
            eth_balance = await self.layerbank_eth_contract.functions.balanceOf(
                self.w3.to_checksum_address(self.address)
            ).call()
            
            tx_data = await self.get_tx_data()
            
            tx = await self.landing_contract.functions.redeemToken(self.layerbank_eth_addr, eth_balance).build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when redeem tokens from LayerBank: {error}', self.account_id, self.address, status='error')
            return False