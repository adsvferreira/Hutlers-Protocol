import { Token } from "../Main"
import { useState } from "react"
import { StakeForm } from "./StakeForm"
import {Box,Tab, makeStyles} from "@material-ui/core"
import { WalletBalance } from "./WalletBalance"
import {TabContext, TabList, TabPanel} from "@material-ui/lab"

interface YourWalletProps {
    supportedTokens: Array<Token>
}

const useStyles = makeStyles((theme)=>({
    tabContent: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: theme.spacing(4)
    },
    box: {
        backgroundColor: "white",
        borderRadius: "25px"
    },
    header: {
        color: "white"
    }
}))

export const YourWallet = ({ supportedTokens } : YourWalletProps) => {
    //creates state var selectedTokenIndex and set method to update it
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    const handleChange = (event: React.ChangeEvent<{}>, newValue:string) => { 
        setSelectedTokenIndex(parseInt(newValue))
    }

    const classes = useStyles()
    
    return (
        <Box>
            <h1 className={classes.header}>Your Wallet</h1>
            <Box className={classes.box}>
                <TabContext value={selectedTokenIndex.toString()}>
                    <TabList onChange={handleChange} aria-label="stake form tabs">
                        {supportedTokens.map((token, index)=> {
                            return (
                                <Tab label={token.name}
                                    value={index.toString()}
                                    key={index} />
                            )
                        })}
                    </TabList>
                    {supportedTokens.map((token, index) => {
                        return (
                            <TabPanel value={index.toString()} key={index}>
                                <div className={classes.tabContent}>
                                    <WalletBalance token={supportedTokens[selectedTokenIndex]}/>
                                    <StakeForm token={supportedTokens[selectedTokenIndex]}/>
                                </div>
                            </TabPanel>
                        )
                    })}
                </TabContext>
            </Box>
        </Box>
    )    
}