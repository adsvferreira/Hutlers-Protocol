// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    // stakeTokens
    // unStakeTokens
    // issueTokens
    // addAllowedTokens
    // getUserTVL (USD)

    mapping(address => uint256) public uniqueTokensStaked;
    mapping(address => address) public tokenPriceFeedMapping;
    // mapping token_address -> staker_address -> amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
    address[] public stakers;
    address[] public allowedTokens;
    IERC20 public dappToken;

    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function setPriceFeedAddress(address _token, address _priceFeedAddress)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeedAddress;
    }

    function stakeTokens(uint256 _amount, address _token) public {
        // what tokens can be staked?
        // how much can be staked ?
        require(_amount > 0, "Amount must be greater than 0");
        require(tokenIsAllowed(_token), "Token is currently not allowed");
        // instantiate IERC20 instance with _token address in order to use functions in ABI:
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokensStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) public {
        // Note: stakers list is not being updated
        // Delete an entry from an array in solidity without leave a "0"
        // in that position is not trivial and might get gas expensive
        // We're already checking this before issue token rewards
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance must be greater than 0");
        IERC20(_token).transfer(msg.sender, balance);
        // Update balances after a token transfer -> Vulnerable to reentrancy attack
        // TODO: Fix this later
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;
    }

    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }
        return false;
    }

    function issueTokens() public onlyOwner {
        // Issue tokens to all stakers
        for (
            uint256 stakerIndex = 0;
            stakerIndex < stakers.length;
            stakerIndex++
        ) {
            address recipient = stakers[stakerIndex];
            //######################################################################
            // send each taker a token reward based on tvl
            // 1 USD in tvl => 1 DappToken
            //######################################################################
            // it's very gas expensive to loop through all users and staked tokens
            // and then send the tokens to the right addresses
            // that's why protocols use to have a separate claim rewards function
            // triggered by the user
            uint256 userTVL = getUserTVL(recipient);
            dappToken.transfer(recipient, userTVL);
        }
    }

    function getUserTVL(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No tokens staked!");
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _user,
                    allowedTokens[allowedTokensIndex]
                );
            return totalValue;
        }
    }

    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        // 1 ETH -> $2,000
        // >> 2000
        // 200 DAI -> $200
        // >> 200
        if (uniqueTokensStaked[_user] <= 0) {
            return 0;
        }
        // price of the token * stakingBalance[_token][user]
        (uint256 price, uint256 decimals) = getTokenValueAndDecimals(_token);
        // 1.000.000.000.000.000.000 ETH (18 decimals)
        // ETH/USD -> 100.000.000 (6 decimals)
        return ((stakingBalance[_token][_user] * price) / (10**decimals));
    }

    function getTokenValueAndDecimals(address _token)
        public
        view
        returns (uint256, uint256)
    {
        //priceFeedAddress
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }
}
