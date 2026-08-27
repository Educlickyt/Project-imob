import React from 'react'
import styles from './Menu.module.css';
import { Link } from 'react-router-dom';


const Menu = () => {
  return (
    <>
        <aside className={styles.sidebar}>
            <div className={styles.logo}>
                <img src="/public/Logo_colapsed.svg" alt="Logo do sistema" />
                <img src="/public/Logo_text.svg" alt="Logo do sistema" />

            </div>

            <nav className={styles.sidebar_nav}>
                <ul className={styles.menu}>
                    <li className={styles.menu_item}>
                        <Link to={'/dashboard'} className={`${styles.menu_link} ${styles.active}`}>
                            <img className={styles.icon} src="/public/ActiveDashboard_icon.svg" alt="" />
                            <span className={styles.menu_text}>Dashboard</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/properties'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Properties_icon.svg" alt="" />
                            <span className={styles.menu_text}>Imóveis</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/leads'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Leads_icon.svg" alt="" />
                            <span className={styles.menu_text}>Leads</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/clients'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Clients_icon.svg" alt="" />
                            <span className={styles.menu_text}>Clientes</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/property-owners'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Owners_icon.svg" alt="" />
                            <span className={styles.menu_text}>Proprietários</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/tenant-users'} className={styles.menu_link}>
                            <img className={styles.icon} src="/public/Users_icon.svg" alt="" />
                            <span className={styles.menu_text}>Colaboradores</span>
                        </Link>
                    </li>
                    <li className={styles.menu_item}>
                        <Link to={'/settings'} className={styles.menu_link}>
                            <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <circle cx="12" cy="12" r="3" />
                                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
                            </svg>
                            <span className={styles.menu_text}>Configurações</span>
                        </Link>
                    </li>
                    
                </ul>
            </nav>
        </aside>
        <div className={styles.bgFilter}></div>
    </>


  )
}

export default Menu