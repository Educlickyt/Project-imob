import React from 'react'
import Header from '../components/header/Header'
import HeroBanner from '../components/heroBanner/HeroBanner'

const LandingPage = ({ onLoginClick }) => {
  return (
    <>
        <Header onLoginClick={onLoginClick} />
        <HeroBanner/>
    </>
  )
}

export default LandingPage;