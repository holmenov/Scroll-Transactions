import random

from modules.account import Account
from utils.config import NFTS2ME_ABI
from utils.wrappers import check_gas
from utils.utils import send_logs

class NFT2Me(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id, private_key, proxy)
    
    @check_gas
    async def mint(self, contracts: dict):
        try:
            send_logs(f'Mint NFT on NFTS2ME.', self.account_id, self.address)
            
            nft_data = random.choice(list(contracts.items()))
            nft_contract, nft_price = nft_data
            
            price = self.w3.to_wei(nft_price, 'ether')
            contract = self.get_contract(nft_contract, NFTS2ME_ABI)
            
            tx_data = await self.get_tx_data()
            tx_data.update({'value': price})
            
            tx = await contract.functions.mint().build_transaction(tx_data)
            
            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when using NFTS2ME: {error}', self.account_id, self.address, status='error')
            return True # It's not a typo, nft2me sometimes generates errors