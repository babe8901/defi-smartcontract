from brownie import (
    accounts,
    network,
    config,
    Contract,
    MockDAI,
    MockWETH,
    MockV3Aggregator,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
INITIAL_PRICE_FEED_VALUE = 2000000000000000000000
DECIMALS = 18


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "fau_token": MockDAI,
    "weth_token": MockWETH,
}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to use for a network that doesn't have the contract
    Args:
        contract_name (string): This is the name of the contract that we will get
        from the config or deploy
    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        Contract of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_PRICE_FEED_VALUE):
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()

    print("Deloying Mock Price Feed...")
    price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print(f"Mock price feed deployed to {price_feed.address}")

    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Mock DAI deployed to {dai_token.address}")

    print("Deploying Mock WETH...")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Mock WETH deployed to {weth_token.address}")

    print("All done!")
