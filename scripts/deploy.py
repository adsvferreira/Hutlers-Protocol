import os
import yaml
import json
import shutil
from web3 import Web3
from scripts.helpers import get_account, get_contract
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import FerreraToken, TokenFarm, network, config

KEPT_BALANCE = Web3.toWei(25000000, "ether")


def deploy_token_farm_and_token(update_frontend=False):
    account = get_account()
    ferrera_token = FerreraToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        ferrera_token.address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify")
    )
    tx = ferrera_token.transfer(token_farm.address, ferrera_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)
    # dapp_token, weth_token, fau_token/dai (faucet token - we can mint any amount for testing)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    allowed_tokens_dict = {
        ferrera_token: get_contract("dai_usd_price_feed"),  # for testing: ferrera token price = dai
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, allowed_tokens_dict, account)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS and update_frontend:
        update_frontend()
    return token_farm, ferrera_token


def add_allowed_tokens(token_farm, allowed_tokens_dict, account):
    for token in allowed_tokens_dict:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_price_feed_tx = token_farm.setPriceFeedAddress(token.address, allowed_tokens_dict[token], {"from": account})
        set_price_feed_tx.wait(1)
    return token_farm


def update_frontend():
    """
    Sends the build folder to frontend dir
    Sends our config.yaml file to frontend dir in JSON format
    This works only because we've contracts and frontend in the same repo
    """
    copy_folders_to_frontend("./build", "./frontend/src/chain-info")
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./frontend/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print("Frontend updated!")


def copy_folders_to_frontend(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # delete dest folder if already exists
    shutil.copytree(src, dest)  # copy src folder into dest folder


def main():
    deploy_token_farm_and_token(update_frontend=True)
