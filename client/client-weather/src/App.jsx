import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

import TempDisplay from './components/TemperatureDisplay'

import HourlyDisplay from './components/HourlyTempDisplay'

import NextTemps from './components/NextTempsDisplay'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <TempDisplay/>
      <HourlyDisplay/>
      <NextTemps/>
    </div>
    
  )
}

export default App
