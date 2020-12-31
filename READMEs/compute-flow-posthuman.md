# Quickstart: Marketplace Flow with compute-to-data for Posthuman

This tutorial demonstrates publishing a dataset with `compute` service.
The data asset used is a pre-trained GPT-2 Model, which is used to provide compute_service_evaluate, using the algorithim algo_eval_wikitext.py .

As we are utilising large transformer models, for end-to-end testing this requires Alice to be running a kubernetes cluster at localhost:8080, with at least 1 NVIDIA-V100 GPU. In posthuman, the marketplace will serve Alice's role; users need only worry about the process followed by Bob from step 3 on.

We will be connecting to the `rinkeby` test net and the Ocean Protocol 
supporting services.

Here's the steps:
1. Setup
1. Alice publishes assets for data services (= publishes a datatoken contract and metadata)
1. Value swap: Bob buys datatokens from marketplace
1. Bob uses a service by spending datatoken he just purchased (Compute)

Let's go through each step.

## 0. Prerequisites and Installation
Use an ethereum account with some eth balance on rinkeby. You can get rinkeby eth using 
this [faucet](https://www.rinkeby.io/#faucet). Otherwise, run `ganache-cli` and replace 
`rinkeby` with `ganache` when following the steps below.

If you haven't installed yet:
```console
pip install ocean-lib
```

## 1. Initialize services

This quickstart treats the publisher/provider service, metadata cache, and marketplace as 
externally-run services. For convenience, we run them locally. Refer to each repo for 
its own requirements and make sure they all point to `rinkeby` testnet.

[Provider service](https://github.com/oceanprotocol/provider-py)
```
docker run @oceanprotocol/provider-py:latest
```

[Aquarius (Metadata cache)](https://github.com/oceanprotocol/aquarius)

```
docker run @oceanprotocol/aquarius:latest
```

[Market app](https://github.com/oceanprotocol/market)
```
git clone https://github.com/oceanprotocol/market.git
cd market
npm install
npm start
```
Access the market app in the browser at `http://localhost:8000`.

## 1b. ENV setup
export the following env variables, including credentials for two Rinkerby wallets:
```
export NETWORK_URL=''
export Publisher_Key=''
export Consumer_Key=''

## 2A. Perform imports
```
python
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

from examples.compute_service import build_compute_descriptor, get_config_dict, run_compute, publish_asset
```

## 2. Alice publishes assets for data services (= publishes a DataToken contract), Mints 100 tokens, and creates a pool

```ocean = Ocean(config=Config(options_dict=get_config_dict()))
        publisher = Wallet(ocean.web3, private_key='0xc594c6e5def4bab63ac29eed19a134c130388f74f019bc74b8f4389df2837a58')  # 0xe2DD09d719Da89e5a3D0F2549c7E24566e947260
        #consumer = Wallet(ocean.web3, private_key='0x9bf5d7e4978ed5206f760e6daded34d657572bd49fa5b3fe885679329fb16b16')  # 0x068Ed00cF0441e4829D9784fCBe7b9e26D4BD8d0
        publisher_wallet = Wallet(ocean.web3, private_key=os.getenv('Publisher_Key')) #addr: 0xc966Ba2a41888B6B4c5273323075B98E27B9F364
        consumer = Wallet(ocean.web3, private_key=os.getenv('Consumer_Key')) #addr: 0xEF5dc33A53DD2ED3F670B53F07cEc5ADD4D80504
        pool_address=''
        did=''
        if not (did and pool_address):
            metadata_file = './examples/data/metadata_original_model.json' #GPT-2 Pretrained Meta Data
            with open(metadata_file) as f:
                metadata = json.load(f)

            asset, pool = publish_asset(metadata, publisher_wallet)
            #Dataset asset created successfully: #did=did:op:784Cc17176533cc962cf659B9f49349ba6F9df3b, #datatoken=0x784Cc17176533cc962cf659B9f49349ba6F9df3b
            #pool_address = 0x3490DDd035B2e1DA30Af09AB6090Bf71fdb94898
        else:
            asset = ocean.assets.resolve(did)
            pool = BPool(pool_address)

        if not asset:
            print(f'publish asset failed, cannot continue with running compute.')
            return
```


```


## 4. Value swap: Bob buys datatokens from marketplace (using datatoken <> OCEAN balancer pool)

```python
from ocean_lib.ocean.util import to_base_18
from ocean_lib.web3_internal.wallet import Wallet

bob_wallet = Wallet(ocean.web3, private_key="PASTE BOB'S TEST PRIVATE KEY HERE")
data_token = market_ocean.get_data_token(token_address)
# This assumes bob_wallet already has sufficient OCEAN tokens to buy the data token. OCEAN tokens 
# can be obtained through a crypto exchange or an on-chain pool such as balancer or uniswap
market_ocean.pool.buy_data_tokens(
    pool_address, 
    amount=1.0, # buy one data token
    max_OCEAN_amount=price_in_OCEAN, # pay maximum 0.1 OCEAN tokens
    from_wallet=bob_wallet
)

print(f'bob has {data_token.token_balance(bob_wallet.address} datatokens.')
```
   
## 5. Bob uses compute service of GPT-2 to further train it for 500 steps in exchange for 1 datatoken

```python
#Bob Consumes Service
#Testing code
bob_wallet = Wallet(ocean.web3, private_key=os.getenv('Consumer_Key'))
data_token = market_ocean.get_data_token(token_address)

market_ocean.pool.buy_data_tokens(
    pool_address, 
    amount=1.0, # buy one data token
    max_OCEAN_amount=price_in_OCEAN+0.1, # with buffer
    from_wallet=bob_wallet
)



print(f'bob has {data_token.token_balance(bob_wallet.address)} datatokens.')

quote = ocean.assets.order(asset.did, bob_wallet.address, service_index=service.index)
order_tx_id = market_ocean.assets.pay_for_service(
    quote.amount, quote.data_token_address, asset.did, service.index, market_address, bob_wallet
)
print(f'Requesting compute using asset {asset.did} and pool {pool.address}')
algo_file = './examples/data/Algo_eval_wikitext.py'
job_id, status = run_compute(asset.did, consumer, algo_file, pool.address, order_tx_id)
print(f'Compute started on asset {asset.did}: job_id={job_id}, status={status}')
```

