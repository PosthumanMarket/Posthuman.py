
import warnings

from . import bconstants
from ocean_lib.ocean import util
from ocean_lib.web3_internal.wallet import Wallet
    

class BFactory:    
    def __init__(self, web3, contract_address: str):
        abi = self._abi()
        self.contract = web3.eth.contract(address=contract_address, abi=abi)
    
    def _abi(self):
        return util.abi(filename='./abi/BFactory.abi')
        
    #============================================================
    #reflect BFactory Solidity methods
    def newBPool(self, from_wallet: Wallet) -> str:
        print("BPool.newSPool(). Begin.")
        controller_address = from_wallet.address
        func = self.contract.functions.newBPool(controller_address)
        gaslimit = bconstants.GASLIMIT_BFACTORY_NEWBPOOL
        (_, tx_receipt) = util.buildAndSendTx(func, from_wallet, gaslimit)

        # grab pool_address
        warnings.filterwarnings("ignore") #ignore unwarranted warning up next
        rich_logs = self.contract.events.BPoolCreated().processReceipt(tx_receipt)
        warnings.resetwarnings()
        pool_address = rich_logs[0]['args']['newBPoolAddress']
        print(f"  pool_address = {pool_address}")

        print("BPool.newSPool(). Done.")
        return pool_address
