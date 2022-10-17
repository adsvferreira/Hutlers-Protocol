import {constants, utils} from "ethers"
import { useEffect, useState } from "react"
import {Contract} from "@ethersproject/contracts"
import {useEthers, useContractFunction} from "@usedapp/core"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import networkMapping from "../chain-info/deployments/map.json"
import ERC20 from "../chain-info/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.4.1/ERC20.json"

export const useStakeTokens = (tokenAddress: string) => {
    // address
    // abi
    // chainId
    const { chainId } = useEthers()
    const { abi } = TokenFarm
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero
    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)

    const erc20ABI = ERC20.abi
    const erc20Interface = new utils.Interface(erc20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)    
    // aprove
    // send - contract function being used | state - state of the transaction
    const {send: approveErc20Send, state: approveAndStakeErc20State} = useContractFunction(erc20Contract, "approve", {transactionName: "Approve ERC20 transfer"})
    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        return approveErc20Send(tokenFarmAddress, amount)
    }
    // stake tokens
    const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stakeTokens", {transactionName: "Stake Tokens"})
    const [amountToStake, setAmountToStake] = useState("0")


    //useEffect(func, array) - Run func when var in array changes
    useEffect(() => {
        if(approveAndStakeErc20State.status === "Success") {
            stakeSend(amountToStake, tokenAddress)
        }
    }, [approveAndStakeErc20State, amountToStake, tokenAddress])
    
    const [state, setState] = useState(approveAndStakeErc20State)

    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            setState(stakeState)
        } else {
            setState(approveAndStakeErc20State)
        }
    }, [approveAndStakeErc20State, stakeState])

    return { approveAndStake, state }
}