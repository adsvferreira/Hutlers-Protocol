import { Token } from "../Main"
import { BalanceMsg } from "../BalanceMsg"
import { formatUnits} from "@ethersproject/units"
import { useEthers, useTokenBalance } from "@usedapp/core"

export interface WalletBalanceProps {token: Token}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    const tokenBalance = useTokenBalance(address, account)
    const formatedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 0
    console.log(tokenBalance?.toString())
    return (
    <BalanceMsg
        label={`Available ${name} balance`}
        tokenImgSrc={image}
        amount={formatedTokenBalance}
    />)
}