#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

# Allows Charlie to further fine-tune a model created by Alice on a new dataset.

#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

#Allows bob to purchase inference from the model Alice posted. Requires dt and compute_ddo as arguments

import uuid

from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes

from ocean_lib.assets.asset import Asset
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_lib.models.algorithm_metadata import AlgorithmMetadata
from tests.resources.helper_functions import (
    get_consumer_wallet,
    get_publisher_wallet,
    get_publisher_ocean_instance,
    get_consumer_ocean_instance,
    mint_tokens_and_wait, get_resource_path, wait_for_ddo)

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
import json

from examples.compute_service import build_compute_descriptor, run_compute, publish_asset

# Fine-tuning algorithim: requires INPUT_FILE_LINK and INPUT_FILE env vars., defining the input plaintext file for further training.

fp = "examples/data/metadata_training.json"
algorithm_meta = json.load(open(fp))


def get_config_dict():
    return {
        'eth-network': {
            'network': 'rinkeby',
        },
        'resources': {
            'aquarius.url': 'https://aquarius.rinkeby.oceanprotocol.com',
            'provider.url': 'http://18.217.14.245:8030/'  # Posthuman Marketplace Provider for GPU access
        }
    }

def test_compute_flow(dt, compute_ddo):
    ######
    # setup
    c_ocean_instance = Ocean(config=Config(options_dict=get_config_dict()))
    consumer_wallet = Wallet(ocean.web3, private_key=os.getenv('Consumer_Key'))
    #c_ocean_instance = get_consumer_ocean_instance()
    cons_ocn = c_ocean_instance
    #consumer_wallet = get_consumer_wallet()

    # Define DT address
    ######
    # Give the consumer some datatokens so they can order the service
    try:
        tx_id = dt.transfer_tokens(consumer_wallet.address, 10, pub_wallet)
        dt.verify_transfer_tx(tx_id, pub_wallet.address, consumer_wallet.address)
    except (AssertionError, Exception) as e:
        print(e)
        raise

    ######
    # Order compute service from the dataset asset
    order_requirements = cons_ocn.assets.order(
        compute_ddo.did,
        consumer_wallet.address,
        service_type=ServiceTypes.CLOUD_COMPUTE
    )

    ######
    # Start the order on-chain using the `order` requirements from previous step
    service = compute_ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
    _order_tx_id = cons_ocn.assets.pay_for_service(
        order_requirements.amount,
        order_requirements.data_token_address,
        compute_ddo.did,
        service.index,
        '0xc966Ba2a41888B6B4c5273323075B98E27B9F364',
        consumer_wallet
    )
    #update marketplace address

    ######
    job_id = cons_ocn.compute.start(
        did, consumer_wallet, _order_tx_id,
        nonce=order_requirements.nonce, algorithm_meta=algorithm_meta)
    assert job_id, f'expected a job id, got {job_id}'

    status = cons_ocn.compute.status(did, job_id, consumer_wallet)
    print(f'got job status: {status}')
    assert status and status['ok'], f'something not right about the compute job, got status: {status}'

    status = cons_ocn.compute.stop(did, job_id, consumer_wallet)
    print(f'got job status after requesting stop: {status}')
    assert status, f'something not right about the compute job, got status: {status}'

