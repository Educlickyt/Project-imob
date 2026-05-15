import React from 'react'
import Style from './Header.module.css'
import {Link} from 'react-router-dom'

const Header = () => {
  return (
    <header className={Style.header}>
      <Link to='/' className={Style.logo}></Link>
      <nav>
        <div>
          <Link to="/about">Sobre nós</Link>
          <Link to="/contact">Contato</Link>
          <Link to="/blog">Blog</Link>
        </div>
        <Link to="/login"><button>Entrar</button></Link>    
      </nav>
    </header>
  )
}

export default Header