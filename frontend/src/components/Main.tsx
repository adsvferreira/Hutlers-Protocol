import logo from "../logo.png"
import {constants} from "ethers"
import eth_logo from "../eth_logo.png"
import dai_logo from "../dai_logo.png"
import {YourWallet} from "./yourWallet"
import {useEthers} from "@usedapp/core"
import {makeStyles} from "@material-ui/core"
import helperConfig from "../helper-config.json"
import brownieConfig from "../brownie-config.json"
import networkMapping from "../chain-info/deployments/map.json"

export type Token = {
    image: string
    address: string
    name: string
}

const useStyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)
    }
}))

export const Main = () => {
    // Show token values from the wallet
    // Get the address of different tokens
    // Get the balance of the users wallet

    // Send the brownie-config to our "src" folder
    // send the "build" folder
    // const helperConfigAny: any = helperConfig // Not required because "suppressImplicaitAnyIndexErrors": true
    const classes = useStyles()
    const {chainId, error} = useEthers()
    const strChainId = chainId ? String(chainId) : "dev"
    const networkName = helperConfig[strChainId]
    const ferreraTokenAddress = chainId ? networkMapping[strChainId]["FerreraToken"][0] : constants.AddressZero
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero
    const supportedTokens: Array<Token>=[
        {
        image: logo,
        address: ferreraTokenAddress,
        name: "FERR"
        },
        {
        image: eth_logo,
        address: wethTokenAddress,
        name: "WETH"
        },
        {
        image: dai_logo,
        address: fauTokenAddress,
        name: "DAI"
        },
    ]

    return (<>
    <h2 className={classes.title}>Hustle Protocol</h2>
    <YourWallet supportedTokens={supportedTokens}/>
    </>)
}