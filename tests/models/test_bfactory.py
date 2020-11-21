from ocean_lib.ocean import util
from ocean_lib.models.bfactory import BFactory
from ocean_lib.models.bpool import BPool
    
def test1(network, alice_wallet):
    web3 = alice_wallet.web3
    bfactory_address = util.confFileValue(network, 'SFACTORY_ADDRESS')
    bfactory = BFactory(web3, sfactory_address)

    pool_address = bfactory.newBPool(from_wallet=alice_wallet)
    pool = BPool(web3, pool_address)
    assert isinstance(pool, BPool)
    
