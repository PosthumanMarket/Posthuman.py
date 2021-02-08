This README demonstrates how Bob, a model consumer, buys datatokens to access the inference service of Alice's model.
Bob require's Alice's models pool address and datatoken address

## 1. Save asset and pool details
```
token_address = '0x7E227205368243285584a54464fC8A6c2993f5d3'
pool_address = '0x00Dd3F792be3D13a1C728E329Ae7951d9259014e'
did = 'did:op:7E227205368243285584a54464fC8A6c2993f5d3'

token_address = '0x1F625a835f51faFd661cBcc9D35cb1e8fcB55Bd7'
pool_address = '0xa9C03F28A60e29915fECcEEFEC1c37520C0CCE9C'
did = 'did:op:1F625a835f51faFd661cBcc9D35cb1e8fcB55Bd7'

token_address = '0x1d4D92791587968211e990A1FFE51377c8b45D54'
pool_address = '0x37c4e732f99F31b257f9A9d5f8156e328Af30Af5'
did = 'did=did:op:1d4D92791587968211e990A1FFE51377c8b45D54'

#Asset did:op:ba844a436DFE954B042BcD7cd5c934CddC60b011 can now be purchased from pool @0xdF1fB9Ee447ee06f8eBea9F89a3D7E249269C36a at the price of 1.0359473738734073 OCEAN tokens.
```
## 2. Perform Imports
```
import os

from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_utils.agreements.service_factory import ServiceDescriptor
import json

from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.utils.utilities import get_timestamp

from ocean_lib.config import Config
from ocean_lib.models.algorithm_metadata import AlgorithmMetadata
from ocean_lib.models.bpool import BPool
from ocean_lib.models.data_token import DataToken
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.web3_internal.wallet import Wallet
import os

from examples.compute_service_train import build_compute_descriptor, get_config_dict, run_compute, publish_asset
#compute_service_train includes reward mechanism for Charlie

```

```
datatoken liquidity pool was created at address 0x7b6aF8B923DfB1888163c87F416Cf4D1a785710E
Asset did:op:D6F985EB261D232F756424B428654f622AAAB61c can now be purchased from pool @0x7b6aF8B923DfB1888163c87F416Cf4D1a785710E at the price of 1.0359473738734073 OCEAN tokens.
```

```
ocean = Ocean(config=Config(options_dict=get_config_dict()))
market_ocean = ocean
market_address = '0xc966Ba2a41888B6B4c5273323075B98E27B9F364' # Hardcoded market address
bob_wallet = Wallet(ocean.web3, private_key=os.getenv('Consumer_Key'))
data_token = market_ocean.get_data_token(token_address)

#point to service
from ocean_utils.agreements.service_types import ServiceTypes
asset = market_ocean.assets.resolve(did)
service = asset.get_service(ServiceTypes.CLOUD_COMPUTE) 

#point to pool
pool = market_ocean.pool.get(pool_address)

OCEAN_address = market_ocean.OCEAN_address
price_in_OCEAN = market_ocean.pool.calcInGivenOut(
    pool_address, OCEAN_address, token_address, token_out_amount=1.0)
print(f"Price of 1 datatoken is {price_in_OCEAN} OCEAN")
```


## 3. Bob Buys Datatokens
```
market_ocean.pool.buy_data_tokens(
    pool_address, 
    amount=1.0, # buy one data token
    max_OCEAN_amount=price_in_OCEAN+1, # with buffer
    from_wallet=bob_wallet
)
```

## 4. Charlie requests compute (training) using datatokens; recieves tokens (ownership) of newly trained model
```
#export file for evaluation as EVAL_DATA env var
quote = market_ocean.assets.order(asset.did, Alice_wallet.address, service_index=service.index)
fee_receiver = market_address
order_tx_id = bob_ocean.assets.pay_for_service(
    quote.amount, quote.data_token_address, asset.did, service.index, fee_receiver, bob_wallet)
print(f'Requesting compute using asset {asset.did} and pool {pool.address}')
algo_file = '/home/ubuntu/Posthuman.py/examples/data/eval6.py'
job_id, status, asset, pool = run_compute(asset.did, bob_wallet, algo_file, pool.address, order_tx_id)
print(f'Compute started on asset {asset.did}: job_id={job_id}, status={status}')
```

## 5. (Bonus) Bob requests inference using datatokens

```
#Place path to file with inference text in ENV VAR 'INFERENCE_DATA'

quote = market_ocean.assets.order(asset.did, bob_wallet.address, service_index=service.index)
order_tx_id = bob_ocean.assets.pay_for_service(
    quote.amount, quote.data_token_address, asset.did, service.index, fee_receiver, bob_wallet)
print(f'Requesting compute using asset {asset.did} and pool {pool.address}')

algo_file = '../Posthuman.py/examples/data/algo_training.py'
job_id, status = run_compute(asset.did, consumer, algo_file, pool.address, order_tx_id)
print(f'Compute started on asset {asset.did}: job_id={job_id}, status={status}')
```