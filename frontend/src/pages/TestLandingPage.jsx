import React, { useState } from 'react'
import Style from './TestLandingPage.module.css'

const TestLandingPage = () => {
  const [activeCard, setActiveCard] = useState(null)

  const features = [
    {
      id: 1,
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="8" width="40" height="32" rx="4" stroke="currentColor" strokeWidth="2.5"/>
          <path d="M16 8V4H32V8" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
          <path d="M24 20V32M24 32L18 26M24 32L30 26" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
      title: 'Gestao Completa',
      description: 'Gerencie seus imoveis, clientes e documentos em um so lugar. Controle total do seu negocio.',
      buttonLabel: 'Comecar Agora',
      accent: 'primary'
    },
    {
      id: 2,
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="24" cy="16" r="8" stroke="currentColor" strokeWidth="2.5"/>
          <path d="M10 40C10 32.268 16.268 26 24 26C31.732 26 38 32.268 38 40" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
          <path d="M30 14L34 10M38 16L42 12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"/>
        </svg>
      ),
      title: 'Equipe Unida',
      description: 'Colabore em tempo real com sua equipe. Compartilhe informacoes e feche mais vendas juntos.',
      buttonLabel: 'Conhecer Equipe',
      accent: 'secondary'
    },
    {
      id: 3,
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="6" y="6" width="16" height="16" rx="3" stroke="currentColor" strokeWidth="2.5"/>
          <rect x="26" y="6" width="16" height="16" rx="3" stroke="currentColor" strokeWidth="2.5"/>
          <rect x="6" y="26" width="16" height="16" rx="3" stroke="currentColor" strokeWidth="2.5"/>
          <rect x="26" y="26" width="16" height="16" rx="3" stroke="currentColor" strokeWidth="2.5"/>
          <circle cx="14" cy="14" r="3" fill="currentColor"/>
          <circle cx="34" cy="14" r="3" fill="currentColor"/>
          <circle cx="14" cy="34" r="3" fill="currentColor"/>
          <circle cx="34" cy="34" r="3" fill="currentColor"/>
        </svg>
      ),
      title: 'Dashboard Inteligente',
      description: 'Visualize metricas essenciais com graficos e relatorios automaticos que impulsionam decisoes.',
      buttonLabel: 'Ver Dashboard',
      accent: 'tertiary'
    },
    {
      id: 4,
      icon: (
        <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M24 6L30 18H42L32 26L36 38L24 30L12 38L16 26L6 18H18L24 6Z" stroke="currentColor" strokeWidth="2.5" strokeLinejoin="round"/>
        </svg>
      ),
      title: 'Destaque seus Imoveis',
      description: 'Fotos profissionais, tours virtuais e anuncios inteligentes que atraem o comprador ideal.',
      buttonLabel: 'Explorar',
      accent: 'quaternary'
    }
  ]

  const handleCardClick = (id) => {
    setActiveCard(activeCard === id ? null : id)
  }

  return (
    <div className={Style.page}>
      <header className={Style.nav}>
        <div className={Style.logo}>Realestate</div>
        <nav className={Style.navLinks}>
          <a href="#features">Funcionalidades</a>
          <a href="#cta">Planos</a>
          <a href="#footer">Contato</a>
        </nav>
      </header>

      <section className={Style.hero}>
        <div className={Style.heroContent}>
          <span className={Style.badge}>Plataforma #1 do mercado</span>
          <h1 className={Style.heroTitle}>
            Transforme a gestao do seu<br />
            <span className={Style.highlight}>escritorio imobiliario</span>
          </h1>
          <p className={Style.heroSubtitle}>
            A plataforma completa para profissionais do mercado imobiliario.
            Organize, automatize e escale seu negocio com tecnologia de ponta.
          </p>
          <div className={Style.heroButtons}>
            <button className={Style.btnPrimary}>Teste Gratis por 14 Dias</button>
            <button className={Style.btnOutline}>Ver Demonstracao</button>
          </div>
        </div>
        <div className={Style.heroVisual}>
          <div className={Style.visualCard}>
            <div className={Style.statItem}>
              <span className={Style.statNumber}>2.4k+</span>
              <span className={Style.statLabel}>Imoveis gerenciados</span>
            </div>
            <div className={Style.statItem}>
              <span className={Style.statNumber}>98%</span>
              <span className={Style.statLabel}>Satisfacao dos clientes</span>
            </div>
            <div className={Style.statItem}>
              <span className={Style.statNumber}>120+</span>
              <span className={Style.statLabel}>Escritorios ativos</span>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className={Style.features}>
        <div className={Style.sectionHeader}>
          <span className={Style.badge}>Funcionalidades</span>
          <h2>Tudo que voce precisa em uma plataforma</h2>
          <p>Descubra as ferramentas que vao revolucionar a forma como voce trabalha</p>
        </div>
        <div className={Style.cardGrid}>
          {features.map((feature) => (
            <div
              key={feature.id}
              className={`${Style.card} ${activeCard === feature.id ? Style.cardActive : ''}`}
              onClick={() => handleCardClick(feature.id)}
            >
              <div className={`${Style.iconWrap} ${Style[feature.accent]}`}>
                {feature.icon}
              </div>
              <h3 className={Style.cardTitle}>{feature.title}</h3>
              <p className={Style.cardDesc}>{feature.description}</p>
              <button className={`${Style.btnCard} ${Style[feature.accent]}`}>
                {feature.buttonLabel}
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 5L11 9L7 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </div>
          ))}
        </div>
      </section>

      <section id="cta" className={Style.ctaSection}>
        <div className={Style.ctaBox}>
          <h2>Pronto para revolucionar seu negocio?</h2>
          <p>Junte-se a centenas de escritorios que ja transformaram seus resultados com a nossa plataforma.</p>
          <div className={Style.ctaButtons}>
            <button className={Style.btnCtaPrimary}>Comecar Agora - e Gratis</button>
            <button className={Style.btnCtaOutline}>Falar com Consultor</button>
          </div>
        </div>
      </section>

      <footer id="footer" className={Style.footer}>
        <div className={Style.footerContent}>
          <div className={Style.footerBrand}>
            <div className={Style.logo}>Realestate</div>
            <p>A plataforma que conecta pessoas aos seus sonhos.</p>
          </div>
          <div className={Style.footerLinks}>
            <div>
              <h4>Produto</h4>
              <a href="#features">Funcionalidades</a>
              <a href="#cta">Planos</a>
              <a href="#">Integracoes</a>
            </div>
            <div>
              <h4>Empresa</h4>
              <a href="#">Sobre nos</a>
              <a href="#">Blog</a>
              <a href="#">Carreiras</a>
            </div>
            <div>
              <h4>Suporte</h4>
              <a href="#">Central de ajuda</a>
              <a href="#">Contato</a>
              <a href="#">Status</a>
            </div>
          </div>
        </div>
        <div className={Style.footerBottom}>
          <p>&copy; 2026 Realestate. Todos os direitos reservados.</p>
        </div>
      </footer>
    </div>
  )
}

export default TestLandingPage
