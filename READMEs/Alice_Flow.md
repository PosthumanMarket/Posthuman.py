
This README demonstrates how Alice, a model provider, publishes and monetizes her model using Posthuman.


## 1. Setup : Alice runs her own provider on her own hardware to ensure privacy of the model


## 2. Perform imports
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

## 4. Alice publishes a model specified in metadata_model.json as an asset with compute. She mints 100 Datatokens and creates a BPool for trading her DT.
'''
ocean = Ocean(config=Config(options_dict=get_config_dict()))
Alice_wallet = Wallet(ocean.web3, private_key=os.getenv('Alice_Key')) #addr: 0xc966Ba2a41888B6B4c5273323075B98E27B9F364
pool_address=''
did=''
if not (did and pool_address):
    metadata_file = './examples/data/metadata_model.json' #GPT-2 Pretrained Meta Data
    with open(metadata_file) as f:
        metadata = json.load(f)

    asset, pool = publish_asset(metadata, Alice_wallet)
'''






#consumer = Wallet(ocean.web3, private_key=os.getenv('Consumer_Key')) #addr: 0xEF5dc33A53DD2ED3F670B53F07cEc5ADD4D80504
