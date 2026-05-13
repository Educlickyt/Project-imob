import { useState } from 'react'
import { BrowserRouter } from 'react-router-dom'
import './App.css'
import Header from './components/header/Header'
import HeroBanner from './components/heroBanner/HeroBanner'

function App() {

  useEffect(() => {
    fetch("http://localhost:8000")
      .then((res) => res.json())
      .then((data) => setMessage(data.message));
  }, []);

  return (
    <>
    <BrowserRouter>
      <Header/>

      <HeroBanner/>
    </BrowserRouter>
    </>
  )
}

export default App
