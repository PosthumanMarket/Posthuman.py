
[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

<h1 align="center">PostHuman.py</h1>

Posthuman is a Marketplace based on Ocean protocol that allows users to buy compute services on large NLP models. Model Providers contribute funds to train useful models, and Model Consumers purchase inference and evaluation on the models they find most useful. With Posthuman v0.3, Users can now train, infer, and evaluate on any arbitary text data - and utilise the Marketplace Frontend to do so.

Posthuman's decentralised architecture achieves three goals that are impossible with centralised AI providers:
- **Verifiable** Training and Inference: The end user can know for sure which model served a particular inference request
- **Zero-Knowledge** training & ownership: The marketplace controls the models, ensuring each person who contributed to training is rewarded fairly, as all value created by these models remains on-chain and cannot be 'leaked'.
- **Censorship-Resistant** Access : Access to AI is fast becoming a basic necessity for a productive life, however such access can easily be censored by centralised providers. With a decentralised alternative, any holder of crypto is guranteed to be treated equally by the protocol.

Specifically, the workflow for v0.2 is as follows:

1. Alice publishes a GPT-2 model M1 using PostHuman's compute to data provider, trained on any dataset X. [tests/posthuman-legacy/Alice_flow.py]

2. Bob buys datatokens and runs further training (finetuning) on any custom dataset Y, using the algo_training.py algorithm, to create updated model M2. [tests/posthuman-legacy/Charlie_flow.py]

3. The updated model (M2)-
i) remains on the marketplace’s machine;
ii) is published as an asset on ocean
iii) Bob and Alice are rewarded with datatokens of the newly trained model

4. Charlie decides to train the model further, purchasing datatokens from Bob, creating demand.
The second updated model (M3) is likewise published as an asset, and a datatoken reward issued to Charlie [tests/posthuman-legacy/Charlie_flow.py] + [algo_training.py]

5. Derek finds M3 to be sufficiently trained for his commercial use-case. He buys access to the inference endpoints using the DataTokens in Chalie's Possession, completing the demand loop. [tests/posthuman-legacy/Bob_infer_flow.py] + [algo_inference.py]

6. Elena is unsure if the model she is using (M3) is worth what she is paying. She runs an [algo_evaluation.py] C2D request and learns that the model she’s using does indeed have better performance on her dataset than the published SoTA.  [tests/posthuman-legacy/Bob_eval_flow.py]

To get a hands-on understanding, we've developed READMEs for each of these users - check out the README folder.
Furthermore, Posthuman v0.2 now includes a number of tests of the above functionality - check out the tests/posthuman folder.

> Python library to privately & securely publish, exchange, and consume data.

With ocean.py, you can:
- **Publish** data services: downloadable files or compute-to-data.
Ocean creates a new [ERC20](https://github.com/ethereum/EIPs/blob/7f4f0377730f5fc266824084188cc17cf246932e/EIPS/eip-20.md)
datatoken for each dataset / data service.
- **Mint** datatokens for the service
- **Sell** datatokens via an OCEAN-datatoken Balancer pool (for auto price discovery), or for a fixed price
- **Stake** OCEAN on datatoken pools
- **Consume** datatokens, to access the service
- **Transfer** datatokens to another owner, and **all other ERC20 actions**
using [web3.py](https://web3py.readthedocs.io/en/stable/examples.html#working-with-an-erc20-token-contract) etc.

ocean.py is part of the [Ocean Protocol](https://www.oceanprotocol.com) toolset.

This is in beta state and you can expect running into problems. If you run into them, please open up a [new issue](/issues).

- [🏗 Installation](#-installation)
- [🏄 Quickstart](#-quickstart)
  - [Simple Flow](#simple-flow)
  - [Learn more](#learn-more)
  - [Marketplace Flow](#marketplace-flow)
- [🦑 Development](#-development)
- [🏛 License](#-license)

## 🏗 Installation

```pip install ocean-lib```

## 🏄 Quickstart

### Simple Flow

[Publish your first datatoken](READMEs/datatokens_flow.md) - connect to Ethereum, create an Ocean instance, and publish.

### Learn more

- [Get test OCEAN](READMEs/get_test_OCEAN.md) - from rinkeby
- [Understand config parameters](READMEs/parameters.md) - envvars vs files
- [Learn about off-chain services](READMEs/services.md) - Ocean Provider for data services, Aquarius metadata store
- [Learn about wallets](READMEs/wallets.md) - on generating, storing, and accessing private keys
- [Get an overview of ocean-lib](READMEs/overview.md) - key modules and functions

### Marketplace flow

[Create a marketplace and sell data](READMEs/marketplace_flow.md) - batteries-included flow including using off-chain services for metadata and consuming datasets.

## 🦑 Development

If you want to further develop ocean.py, then [please go here](READMEs/developers.md).

## 🏛 License

```
Copyright ((C)) 2021 Ocean Protocol Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
