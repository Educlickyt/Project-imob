import { useEffect, useState } from 'react'
import { BrowserRouter } from "react-router-dom"
import './App.css'

import LandingPage from './pages/LandingPage'

function App() {

  const [message, setMessage] = useState("")

  useEffect(() => {
    fetch("http://localhost:8000")
      .then((res) => res.json())
      .then((data) => setMessage(data.message));
  }, []);

  return (
    <>   
      <BrowserRouter>
        <LandingPage/>
      </BrowserRouter>
    
    </>
  )
}

export default App
