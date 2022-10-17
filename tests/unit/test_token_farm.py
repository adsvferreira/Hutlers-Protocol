import pytest
from brownie import network, exceptions
from scripts.deploy import deploy_token_farm_and_token
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, STARTING_ETH_USD_PRICE, get_account, get_contract


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, token = deploy_token_farm_and_token()
    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedAddress(token.address, price_feed_address, {"from": account})
    # Assert
    assert token_farm.tokenPriceFeedMapping(token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedAddress(token.address, price_feed_address, {"from": non_owner})


def test_stake_tokens(amount_staked):  # amount_staked is defined as a fixture in conftest.py
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, token = deploy_token_farm_and_token()
    # Act
    token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, token.address, {"from": account})
    # Assert
    assert token_farm.stakingBalance(token.address, account.address) == amount_staked
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, token


def issue_tokens(self, amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    account = get_account()
    token_farm, token = test_stake_tokens(amount_staked)
    starting_balance = token.balanceOf(account.address)
    # Act
    token_farm.issueTokens({"from": account})
    # Assert
    # we're staking 1 token == 1 usd price of ETH == STARTING_ETH_USD_PRICE
    assert token.balanceOf(account.address) == starting_balance + STARTING_ETH_USD_PRICE
