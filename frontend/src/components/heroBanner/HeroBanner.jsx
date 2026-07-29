import React from 'react'
import Style from './HeroBanner.module.css'
import heroImage from '../../assets/heroImage.png'
import {Link} from 'react-router-dom'

const HeroBanner = () => {
  return (
    <section className={Style.heroBanner}>
        <div>
          <h1>Seu <b>escritório imobiliário</b>, onde quer que você esteja</h1>
          <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s</p>
          <div>
            <button>Ver Planos</button>
            <Link to=""><button>Periodo de Teste</button></Link>
          </div>
        </div>
        <img src={heroImage} alt="" />
    </section>
  )
}

export default HeroBanner