import React from 'react';
import {Main} from "./components/Main"
import {Header} from "./components/Header"
import {Container} from "@material-ui/core"
import { getDefaultProvider } from 'ethers'
import { DAppProvider, Config, Kovan} from '@usedapp/core';


const config: Config = {
  readOnlyChainId: Kovan.chainId,
  readOnlyUrls: {
    [Kovan.chainId]: getDefaultProvider('kovan'),
  },
  notifications: {
    expirationPeriod: 1000,
    checkInterval: 1000
  }
}

function App(){
  return (
    <DAppProvider config={config}>
      <Header />
        <Container maxWidth="md">
          <Main/>
        </Container>  
    </DAppProvider>
  );
}

export default App;
