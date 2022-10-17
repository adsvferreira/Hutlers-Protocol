import time
from brownie import accounts, network, config, Contract, MockV3Aggregator, MockDAI, MockWETH

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-forked"]
DECIMALS = 8
STARTING_ETH_USD_PRICE = 2000

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "fau_token": MockDAI,
    "weth_token": MockWETH,
}


def get_account(index: int = None, id: str = None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)  # Ex: af_test_account
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name: str):
    """Will grab the contract addresses from the brownie config if defined, otherwise, it will deploy a mock version of that contract (if not deployed yet) and return it

    Args:
    contract_name (string)

    Returns:
        brownie.network.contract.ProjectContract: The most recently deployed version of this contract
    """
    print(f"the active network is {network.show_active()}")
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address
        # ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_ETH_USD_PRICE):
    account = get_account()
    print("Deploying Mocks...")
    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed to {dai_token.address}")
    print("Deploying Mock WETH...")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed to {weth_token.address}")
    print("Deploying Mock V3Aggregator...")
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})

    print("Mocks Deployed!")


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):  # 0.1 LINK
    account = account or get_account()
    link_token = link_token or get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # Or using LINK Token interface:
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract Funded!")
    return tx
