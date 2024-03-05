import random
import string
from loguru import logger

from modules.account import Account
from utils.config import DMAIL_CONTRACT, DMAIL_ABI
from utils.wrappers import check_gas
from utils.utils import send_logs


class Dmail(Account):
    def __init__(self, account_id: int, private_key: str, proxy: str | None) -> None:
        super().__init__(account_id=account_id, private_key=private_key, proxy=proxy)
        
        self.contract = self.get_contract(DMAIL_CONTRACT['dmail'], DMAIL_ABI)
    
    def get_random_string(self, text_end: str = '') -> str:
        letters = string.ascii_lowercase + string.digits
        length = random.randint(5, 15)

        random_str = ''.join(random.choice(letters) for _ in range(length))
        
        if text_end != '':
            random_str = random_str + text_end

        return (random_str.encode()).hex()

    @check_gas
    async def send_mail(self):
        try:
            send_logs(f'Send email via DMail.', self.account_id, self.address)
            
            email = self.get_random_string('@gmail.com')
            theme = self.get_random_string()
            
            data = self.contract.encodeABI('send_mail', args=(email, theme))
            
            tx = await self.get_tx_data()
            tx.update({'data': data, 'to': self.w3.to_checksum_address(DMAIL_CONTRACT)})
            
            await self.execute_transaction(tx)
            
            return True

        except Exception as error:
            send_logs(f'Error when using DMail: {error}', self.account_id, self.address, status='error')
            return False