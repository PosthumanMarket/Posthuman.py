#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

# Allows alice to publish a Model with compute, and recieve some datatokens.
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

from examples.compute_service import build_compute_descriptor, run_compute, publish_asset

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

def test_compute_flow():
    ######
    # setup
    p_ocean_instance = Ocean(config=Config(options_dict=get_config_dict()))
    pub_wallet = Wallet(ocean.web3, private_key=os.getenv('Alice_Key'))
    #c_ocean_instance = get_consumer_ocean_instance()
    #cons_ocn = c_ocean_instance
    #consumer_wallet = get_consumer_wallet()

    ######
    # Publish Assets

    # Dataset with compute service
    sample_ddo_path = get_resource_path('ddo', 'ddo_with_compute_ai.json')
    old_ddo = Asset(json_filename=sample_ddo_path)
    metadata = old_ddo.metadata
    metadata['main']['files'][0]['checksum'] = str(uuid.uuid4())
    service = old_ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
    compute_service = ServiceDescriptor.compute_service_descriptor(
        service.attributes,
        DataServiceProvider.get_url(p_ocean_instance.config)
    )
    block = p_ocean_instance.web3.eth.blockNumber
    compute_ddo = p_ocean_instance.assets.create(
        metadata,
        pub_wallet,
        service_descriptors=[compute_service],
    )
    did = compute_ddo.did

    ddo_reg = p_ocean_instance.assets.ddo_registry()
    log = ddo_reg.get_event_log(ddo_reg.EVENT_METADATA_CREATED, block, compute_ddo.asset_id, 30)
    assert log, f'no ddo created event.'

    ddo = wait_for_ddo(p_ocean_instance, compute_ddo.did)
    assert ddo, f'resolve did {compute_ddo.did} failed.'

    _compute_ddo = p_ocean_instance.assets.resolve(compute_ddo.did)

    # algorithm with download service
    algorithm_ddo_path = get_resource_path('ddo', 'ddo_inference_algorithm.json')
    algo_main = Asset(json_filename=algorithm_ddo_path).metadata['main']
    algo_meta_dict = algo_main['algorithm'].copy()
    algo_meta_dict['url'] = algo_main['files'][0]['url']
    algorithm_meta = AlgorithmMetadata(algo_meta_dict)

    ######
    # Mint tokens for dataset and assign to publisher
    dt = p_ocean_instance.get_data_token(compute_ddo.data_token_address)
    mint_tokens_and_wait(dt, pub_wallet.address, pub_wallet)

    ######
   
