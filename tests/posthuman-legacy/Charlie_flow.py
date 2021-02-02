


token_address = '0x7E227205368243285584a54464fC8A6c2993f5d3'
pool_address = '0x00Dd3F792be3D13a1C728E329Ae7951d9259014e'
did = 'did:op:7E227205368243285584a54464fC8A6c2993f5d3'

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

market_ocean.pool.buy_data_tokens(
    pool_address, 
    amount=1.0, # buy one data token
    max_OCEAN_amount=price_in_OCEAN+0.1, # with buffer
    from_wallet=bob_wallet
)

#Place training text in ENV VAR 'TRAIN_file'; see algo_training.py for other requirements.

quote = market_ocean.assets.order(asset.did, bob_wallet.address, service_index=service.index)
order_tx_id = bob_ocean.assets.pay_for_service(
    quote.amount, quote.data_token_address, asset.did, service.index, fee_receiver, bob_wallet)
print(f'Requesting compute using asset {asset.did} and pool {pool.address}')

algo_file = '../Posthuman.py/examples/data/algo_training.py'
job_id, status = run_compute(asset.did, consumer, algo_file, pool.address, order_tx_id)
print(f'Compute started on asset {asset.did}: job_id={job_id}, status={status}')